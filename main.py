"""Interfaz de consola de Biblioteca UNCP (ejecutar: python3 main.py)."""

from biblioteca import Biblioteca
from models import Electronico, Libro, Producto
from utils.exceptions import NotFoundError, ValidationError


def leer_entero(etiqueta: str) -> int:
    """Transforma errores de conversión en errores controlados de entrada."""
    entrada = input(etiqueta)
    try:
        return int(entrada)
    except ValueError as error:
        raise ValidationError(f"'{entrada}' no es un número entero válido.") from error


def registrar_libro(biblioteca: Biblioteca) -> None:
    print("\n--- Registrar libro ---")
    codigo = input("Código: ")
    nombre = input("Nombre: ")
    precio = input("Precio base (S/): ")
    cantidad = leer_entero("Cantidad: ")
    autor = input("Autor: ")
    isbn = input("ISBN: ")
    libro = Libro(codigo, nombre, precio, cantidad, autor, isbn)
    biblioteca.registrar(libro)
    print(f"Registro exitoso: {libro}")


def registrar_electronico(biblioteca: Biblioteca) -> None:
    print("\n--- Registrar equipo electrónico ---")
    codigo = input("Código: ")
    nombre = input("Nombre: ")
    precio = input("Precio base (S/): ")
    cantidad = leer_entero("Cantidad: ")
    marca = input("Marca: ")
    garantia = leer_entero("Garantía (meses): ")
    equipo = Electronico(codigo, nombre, precio, cantidad, marca, garantia)
    biblioteca.registrar(equipo)
    print(f"Registro exitoso: {equipo}")


def listar_catalogo(biblioteca: Biblioteca) -> None:
    print("\n--- Catálogo ---")
    productos = biblioteca.listar()
    if not productos:
        print("El catálogo está vacío.")
    for producto in productos:
        print(producto)


def buscar_producto(biblioteca: Biblioteca) -> None:
    codigo = input("Código que desea buscar: ")
    print(f"Encontrado: {biblioteca.buscar(codigo)}")


def actualizar_producto(biblioteca: Biblioteca) -> None:
    codigo = input("Código que desea actualizar: ")
    print("1. Precio  2. Cantidad")
    campo = input("Campo: ").strip()
    if campo == "1":
        valor = input("Nuevo precio (S/): ")
        producto = biblioteca.actualizar_precio(codigo, valor)
    elif campo == "2":
        valor = leer_entero("Nueva cantidad: ")
        producto = biblioteca.actualizar_cantidad(codigo, valor)
    else:
        raise ValidationError("Elija 1 (precio) o 2 (cantidad).")
    print(f"Actualización exitosa: {producto}")


def mostrar_precios(biblioteca: Biblioteca) -> None:
    print("\n--- Precios finales (polimorfismo) ---")
    productos = biblioteca.listar()
    if not productos:
        print("El catálogo está vacío.")
    for producto in productos:
        # El despacho dinámico elige el método sin consultar el tipo concreto.
        print(f"{producto.codigo} | {producto.nombre} | "
              f"Precio final: S/ {producto.calcular_precio_final():.2f}")


def demostrar_casos() -> None:
    """Ejemplo aislado para no modificar el catálogo del usuario."""
    ejemplo = Biblioteca()
    ejemplo.registrar(Libro("L-DEMO", "Python básico", 100, 2,
                           "Autora UNCP", "978-0001"))
    ejemplo.registrar(Electronico("E-DEMO", "Lector digital", 200, 1,
                                 "Marca UNCP", 12))
    print("\nCaso exitoso: dos registros en un catálogo de demostración.")
    listar_catalogo(ejemplo)
    mostrar_precios(ejemplo)
    try:
        ejemplo.registrar(Libro("l-demo", "Duplicado", 10, 1,
                               "Autora UNCP", "978-0002"))
    except ValidationError as error:
        print(f"ValidationError controlado: {error}")
    try:
        ejemplo.buscar("NO-EXISTE")
    except NotFoundError as error:
        print(f"NotFoundError controlado: {error}")
    print("Continuidad: la demostración terminó sin cerrar la aplicación.")
    print("MRO Libro:", " -> ".join(cls.__name__ for cls in Libro.__mro__))
    print("MRO Electronico:",
          " -> ".join(cls.__name__ for cls in Electronico.__mro__))


def procesar_operacion(biblioteca: Biblioteca, opcion: str) -> None:
    """Gestiona un ciclo real de menú con try/except/else/finally."""
    acciones = {
        "1": registrar_libro,
        "2": registrar_electronico,
        "3": listar_catalogo,
        "4": buscar_producto,
        "5": actualizar_producto,
        "6": mostrar_precios,
    }
    try:
        if opcion == "7":
            demostrar_casos()
        elif opcion in acciones:
            acciones[opcion](biblioteca)
        else:
            raise ValidationError("Opción inválida. Elija un número del 1 al 8.")
    except (ValidationError, NotFoundError) as error:
        print(f"{type(error).__name__} controlado: {error}")
    else:
        print("Operación completada.")
    finally:
        print("--- Fin de operación; el menú continúa ---")


def mostrar_menu() -> None:
    print("\n=== Biblioteca UNCP ===")
    print("1. Registrar libros")
    print("2. Registrar equipos electrónicos")
    print("3. Listar el catálogo")
    print("4. Buscar producto por código")
    print("5. Actualizar precio o cantidad")
    print("6. Mostrar precios finales")
    print("7. Demostración (éxito y dos errores controlados)")
    print("8. Salir")


def main() -> None:
    biblioteca = Biblioteca()
    print("Catálogo en memoria: los datos no persisten al salir.")
    while True:
        try:
            mostrar_menu()
            opcion = input("Elija una opción: ").strip()
            if opcion == "8":
                print("Hasta luego. Biblioteca UNCP cerrada.")
                break
            procesar_operacion(biblioteca, opcion)
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada finalizada. Biblioteca UNCP cerrada.")
            break


if __name__ == "__main__":
    main()
