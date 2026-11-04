"""Entidad base de productos de la biblioteca."""

from decimal import Decimal

from utils.exceptions import ValidationError
from utils.validators import (
    entero_no_negativo,
    normalizar_codigo,
    precio_no_negativo,
    texto_obligatorio,
)


class Producto:
    """Producto con datos comunes y atributos protegidos por propiedades."""

    def __init__(self, codigo: str, nombre: str, precio: object,
                 cantidad: int) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        codigo = normalizar_codigo(valor)
        if hasattr(self, "_codigo") and codigo != self._codigo:
            raise ValidationError("El código no puede cambiar después del registro.")
        self._codigo = codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = texto_obligatorio(valor, "El nombre")

    @property
    def precio(self) -> Decimal:
        return self._precio

    @precio.setter
    def precio(self, valor: object) -> None:
        self._precio = precio_no_negativo(valor)

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        self._cantidad = entero_no_negativo(valor, "La cantidad")

    def calcular_precio_final(self) -> Decimal:
        """Precio base; las subclases aplican sus reglas académicas."""
        return self.precio

    def __str__(self) -> str:
        return (f"{self.codigo} | {self.nombre} | Precio base: "
                f"S/ {self.precio:.2f} | Cantidad: {self.cantidad}")
