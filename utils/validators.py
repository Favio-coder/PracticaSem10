"""Validadores compartidos por modelos y catálogo."""

from decimal import Decimal, InvalidOperation

from .exceptions import ValidationError


def texto_obligatorio(valor: str, campo: str) -> str:
    """Devuelve un texto limpio o avisa de un campo obligatorio vacío."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValidationError(f"{campo} es obligatorio y no puede estar vacío.")
    return valor.strip()


def normalizar_codigo(valor: str) -> str:
    """Unifica mayúsculas y espacios para evitar códigos duplicados."""
    return texto_obligatorio(valor, "El código").upper()


def precio_no_negativo(valor: object) -> Decimal:
    """Convierte precios válidos a Decimal, rechazando infinitos y NaN."""
    if isinstance(valor, bool):
        raise ValidationError("El precio debe ser un número no negativo.")
    try:
        precio = Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError) as error:
        raise ValidationError("El precio debe ser un número válido.") from error
    if not precio.is_finite() or precio < 0:
        raise ValidationError("El precio debe ser un número no negativo y finito.")
    return precio


def entero_no_negativo(valor: object, campo: str) -> int:
    """Valida enteros no negativos, sin aceptar booleanos como enteros."""
    if isinstance(valor, bool) or not isinstance(valor, int) or valor < 0:
        raise ValidationError(f"{campo} debe ser un entero no negativo.")
    return valor
