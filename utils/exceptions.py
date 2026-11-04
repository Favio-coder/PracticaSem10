"""Errores esperados del dominio de la biblioteca."""


class ValidationError(ValueError):
    """Una entrada o un registro incumple las reglas del catálogo."""


class NotFoundError(LookupError):
    """No existe el producto solicitado en el catálogo."""
