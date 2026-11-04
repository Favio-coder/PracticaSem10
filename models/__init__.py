"""Entidades del catálogo de Biblioteca UNCP."""

from .electronico import Electronico
from .libro import Libro
from .producto import Producto

__all__ = ["Producto", "Libro", "Electronico"]
