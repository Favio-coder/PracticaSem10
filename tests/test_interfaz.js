// Prueba de eventos de la interfaz sin instalar dependencias de Node.
// Node se usa solo para verificar; la página funciona sin él en un navegador.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/);
assert.ok(script, 'Debe existir el JavaScript integrado en index.html');

const elements = new Map();
class Elemento {
  constructor() {
    this.value = '';
    this.textContent = '';
    this.hidden = false;
    this.children = [];
    this.handlers = {};
    this.classList = { toggle() {} };
  }

  addEventListener(evento, funcion) { this.handlers[evento] = funcion; }
  dispatchEvent(evento) { this.handlers[evento.type]?.({ preventDefault() {} }); }
  append(hijo) { this.children.push(hijo); }
  replaceChildren() { this.children = []; }
  reset() { this.value = ''; }
}

const elemento = (id) => {
  if (!elements.has(id)) elements.set(id, new Elemento());
  return elements.get(id);
};
const document = {
  getElementById: elemento,
  createElement: () => new Elemento(),
};
vm.runInNewContext(script[1], {
  document,
  Event: class { constructor(type) { this.type = type; } },
  window: { location: { search: '' } },
  URLSearchParams,
});

const escribir = (campos) => {
  for (const [id, valor] of Object.entries(campos)) elemento(id).value = valor;
};
const activar = (id, tipo = 'submit') => elemento(id).dispatchEvent({ type: tipo });

escribir({
  tipo: 'Libro', codigo: 'l-1', nombre: 'Python', precio: '100', cantidad: '2',
  autor: 'Ada', isbn: '978-1',
});
activar('registro');
assert.match(elemento('mensaje').textContent, /registrado correctamente/);

escribir({
  tipo: 'Electrónico', codigo: 'e-1', nombre: 'Tableta', precio: '200',
  cantidad: '1', marca: 'Lenovo', garantia: '12',
});
activar('registro');
assert.equal(elemento('productos').children.length, 2);

escribir({
  tipo: 'Libro', codigo: 'L-1', nombre: 'Otro', precio: '10', cantidad: '1',
  autor: 'Ada', isbn: '978-2',
});
activar('registro');
assert.match(elemento('mensaje').textContent, /ValidationError/);
assert.equal(elemento('productos').children.length, 2);
assert.equal(elemento('errores').children[0].children[0].textContent, 'Catálogo principal');
assert.equal(elemento('errores').children[0].children[1].textContent, 'ValidationError');

escribir({ 'codigo-buscar': 'NO-EXISTE' });
activar('buscar');
assert.match(elemento('mensaje').textContent, /NotFoundError/);
assert.equal(elemento('errores').children[1].children[1].textContent, 'NotFoundError');

escribir({ 'codigo-actualizar': 'L-1', 'campo-actualizar': 'precio', 'valor-actualizar': '-5' });
activar('actualizar');
assert.equal(elemento('errores').children.length, 3);
escribir({ 'valor-actualizar': '50' });
activar('actualizar');
assert.equal(elemento('productos').children[0].children[4].textContent, 'S/ 45.00');

activar('ejecutar-demo', 'click');
assert.equal(elemento('productos-demo').children.length, 2);
assert.equal(elemento('productos-demo').children[0].children[3].textContent, 'S/ 90.00');
assert.equal(elemento('productos-demo').children[1].children[3].textContent, 'S/ 230.00');
assert.equal(elemento('errores').children.length, 5);
assert.equal(elemento('errores').children[0].children[0].textContent, 'Demostración');
assert.equal(elemento('errores').children[0].children[1].textContent, 'ValidationError');
assert.equal(elemento('errores').children[1].children[1].textContent, 'NotFoundError');
assert.equal(elemento('productos').children.length, 2);

activar('ejecutar-demo', 'click');
assert.equal(elemento('productos-demo').children.length, 2);
assert.equal(elemento('errores').children.length, 5);
console.log('OK: catálogo principal, tablas separadas de demo y errores, repetición sin duplicados.');
