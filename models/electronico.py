"""Equipos electrónicos de la biblioteca."""

from decimal import Decimal

from utils.validators import entero_no_negativo, texto_obligatorio

from .producto import Producto


class Electronico(Producto):
    """Equipo con recargo académico supuesto de 15 % sobre el precio."""

    def __init__(self, codigo: str, nombre: str, precio: object,
                 cantidad: int, marca: str, garantia_meses: int) -> None:
        super().__init__(codigo, nombre, precio, cantidad)
        self.marca = marca
        self.garantia_meses = garantia_meses

    @property
    def marca(self) -> str:
        return self._marca

    @marca.setter
    def marca(self, valor: str) -> None:
        self._marca = texto_obligatorio(valor, "La marca")

    @property
    def garantia_meses(self) -> int:
        return self._garantia_meses

    @garantia_meses.setter
    def garantia_meses(self, valor: int) -> None:
        self._garantia_meses = entero_no_negativo(valor, "La garantía en meses")

    def calcular_precio_final(self) -> Decimal:
        return self.precio * Decimal("1.15")

    def __str__(self) -> str:
        return (f"Electrónico | {super().__str__()} | Marca: {self.marca} "
                f"| Garantía: {self.garantia_meses} meses")
