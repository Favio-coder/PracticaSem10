"""Colección de productos: la biblioteca contiene, no hereda, productos."""

from models.producto import Producto
from utils.exceptions import NotFoundError, ValidationError
from utils.validators import normalizar_codigo


class Biblioteca:
    """Catálogo en memoria indexado por códigos normalizados."""

    def __init__(self) -> None:
        self._productos: dict[str, Producto] = {}

    def registrar(self, producto: Producto) -> None:
        if not isinstance(producto, Producto):
            raise ValidationError("Solo se pueden registrar productos.")
        if producto.codigo in self._productos:
            raise ValidationError(f"El código {producto.codigo} ya está registrado.")
        self._productos[producto.codigo] = producto

    def buscar(self, codigo: str) -> Producto:
        codigo = normalizar_codigo(codigo)
        try:
            return self._productos[codigo]
        except KeyError as error:
            raise NotFoundError(f"No existe un producto con código {codigo}.") from error

    def listar(self) -> list[Producto]:
        return list(self._productos.values())

    def actualizar_precio(self, codigo: str, valor: object) -> Producto:
        producto = self.buscar(codigo)
        producto.precio = valor
        return producto

    def actualizar_cantidad(self, codigo: str, valor: int) -> Producto:
        producto = self.buscar(codigo)
        producto.cantidad = valor
        return producto
