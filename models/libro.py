"""Libros del catálogo bibliográfico."""

from decimal import Decimal

from utils.validators import texto_obligatorio

from .producto import Producto


class Libro(Producto):
    """Libro con descuento académico supuesto de 10 % sobre el precio."""

    def __init__(self, codigo: str, nombre: str, precio: object,
                 cantidad: int, autor: str, isbn: str) -> None:
        super().__init__(codigo, nombre, precio, cantidad)
        self.autor = autor
        self.isbn = isbn

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str) -> None:
        self._autor = texto_obligatorio(valor, "El autor")

    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, valor: str) -> None:
        self._isbn = texto_obligatorio(valor, "El ISBN")

    def calcular_precio_final(self) -> Decimal:
        return self.precio * Decimal("0.90")

    def __str__(self) -> str:
        return f"Libro | {super().__str__()} | Autor: {self.autor} | ISBN: {self.isbn}"
