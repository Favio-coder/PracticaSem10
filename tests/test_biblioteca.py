"""Pruebas del dominio y de la ejecución real de la CLI."""

import subprocess
import sys
import unittest
from decimal import Decimal
from pathlib import Path

from biblioteca import Biblioteca
from models import Electronico, Libro, Producto
from utils.exceptions import NotFoundError, ValidationError


RAIZ = Path(__file__).resolve().parents[1]


class PruebasBiblioteca(unittest.TestCase):
    def setUp(self) -> None:
        self.biblioteca = Biblioteca()
        self.libro = Libro(" l-1 ", "Python", "100", 3, "Ada", "978-1")
        self.equipo = Electronico("e-1", "Tableta", "200", 2,
                                  "Lenovo", 12)

    def ejecutar_cli(self, entradas: str) -> str:
        proceso = subprocess.run(
            [sys.executable, "main.py"], input=entradas, text=True,
            capture_output=True, cwd=RAIZ, check=True, timeout=10,
        )
        self.assertNotIn("Traceback", proceso.stderr + proceso.stdout)
        return proceso.stdout

    def test_importaciones_y_herencia(self) -> None:
        self.assertIsInstance(self.libro, Producto)
        self.assertIsInstance(self.equipo, Producto)

    def test_registro_listado_y_busqueda(self) -> None:
        self.biblioteca.registrar(self.libro)
        self.biblioteca.registrar(self.equipo)
        self.assertEqual(len(self.biblioteca.listar()), 2)
        self.assertIs(self.biblioteca.buscar(" l-1 "), self.libro)
        self.assertIs(self.biblioteca.buscar("E-1"), self.equipo)

    def test_duplicado_normalizado_no_sobrescribe(self) -> None:
        self.biblioteca.registrar(self.libro)
        with self.assertRaisesRegex(ValidationError, "ya está registrado"):
            self.biblioteca.registrar(Libro("L-1", "Otro", 5, 1,
                                            "Ada", "978-2"))
        self.assertEqual(self.biblioteca.buscar("L-1").nombre, "Python")

    def test_codigo_no_cambia_tras_registro(self) -> None:
        self.biblioteca.registrar(self.libro)
        with self.assertRaises(ValidationError):
            self.libro.codigo = "L-OTRO"
        self.assertIs(self.biblioteca.buscar("L-1"), self.libro)

    def test_busqueda_y_actualizacion_inexistentes(self) -> None:
        with self.assertRaises(NotFoundError):
            self.biblioteca.buscar("NADA")
        with self.assertRaises(NotFoundError):
            self.biblioteca.actualizar_precio("NADA", 5)
        with self.assertRaises(NotFoundError):
            self.biblioteca.actualizar_cantidad("NADA", 5)

    def test_propiedades_actualizacion_y_polimorfismo(self) -> None:
        self.biblioteca.registrar(self.libro)
        self.biblioteca.registrar(self.equipo)
        self.biblioteca.actualizar_precio("l-1", "50")
        self.biblioteca.actualizar_cantidad("E-1", 9)
        self.assertEqual(self.libro.precio, Decimal("50"))
        self.assertEqual(self.equipo.cantidad, 9)
        precios = [producto.calcular_precio_final()
                   for producto in self.biblioteca.listar()]
        self.assertEqual(precios, [Decimal("45.00"), Decimal("230.00")])

    def test_precio_negativo_no_modifica_producto(self) -> None:
        with self.assertRaises(ValidationError):
            self.libro.precio = -1
        self.assertEqual(self.libro.precio, Decimal("100"))

    def test_precio_invalido_y_no_finito(self) -> None:
        for valor in ("abc", "NaN", "Infinity", True):
            with self.subTest(valor=valor), self.assertRaises(ValidationError):
                self.equipo.precio = valor

    def test_cantidad_invalida(self) -> None:
        for valor in (-1, 1.5, "2", True):
            with self.subTest(valor=valor), self.assertRaises(ValidationError):
                self.libro.cantidad = valor

    def test_campos_obligatorios_y_garantia(self) -> None:
        for campo, valor in (("nombre", "  "), ("autor", " "),
                             ("isbn", ""), ("codigo", "")):
            with self.subTest(campo=campo), self.assertRaises(ValidationError):
                setattr(self.libro, campo, valor)
        with self.assertRaises(ValidationError):
            self.equipo.marca = " "
        with self.assertRaises(ValidationError):
            self.equipo.garantia_meses = -1

    def test_mro(self) -> None:
        self.assertEqual(Libro.__mro__, (Libro, Producto, object))
        self.assertEqual(Electronico.__mro__, (Electronico, Producto, object))

    def test_menu_inicio_salida(self) -> None:
        salida = self.ejecutar_cli("8\n")
        self.assertIn("=== Biblioteca UNCP ===", salida)
        self.assertIn("Hasta luego", salida)

    def test_cli_registro_busqueda_listado_y_precios(self) -> None:
        entradas = ("1\nL-1\nPython\n100\n2\nAda\n978-1\n"
                    "2\nE-1\nTableta\n200\n1\nLenovo\n12\n"
                    "3\n4\nl-1\n6\n8\n")
        salida = self.ejecutar_cli(entradas)
        self.assertIn("Registro exitoso: Libro | L-1", salida)
        self.assertIn("Registro exitoso: Electrónico | E-1", salida)
        self.assertIn("Encontrado: Libro | L-1", salida)
        self.assertIn("Precio final: S/ 90.00", salida)
        self.assertIn("Precio final: S/ 230.00", salida)

    def test_cli_errores_controlados_y_continuidad(self) -> None:
        entradas = ("1\nL-1\nPython\n100\n2\nAda\n978-1\n"
                    "1\nl-1\nOtro\n10\n1\nAda\n978-2\n"
                    "4\nNO-EXISTE\n3\n8\n")
        salida = self.ejecutar_cli(entradas)
        self.assertIn("ValidationError controlado: El código L-1", salida)
        self.assertIn("NotFoundError controlado:", salida)
        self.assertIn("--- Catálogo ---", salida)
        self.assertIn("Hasta luego", salida)

    def test_cli_entrada_numerica_y_precio_negativo(self) -> None:
        entradas = ("1\nL-1\nPython\n-5\n2\nAda\n978-1\n"
                    "1\nL-2\nPython\n5\nxyz\n"
                    "1\nL-3\nPython\n5\n-1\nAda\n978-3\n"
                    "1\nL-4\nPython\nabc\n1\nAda\n978-4\n3\n8\n")
        salida = self.ejecutar_cli(entradas)
        self.assertGreaterEqual(salida.count("ValidationError controlado"), 4)
        self.assertIn("no es un número entero válido", salida)
        self.assertIn("El catálogo está vacío", salida)
        self.assertIn("Hasta luego", salida)

    def test_cli_actualizacion_con_setters(self) -> None:
        entradas = ("1\nL-1\nPython\n100\n2\nAda\n978-1\n"
                    "5\nL-1\n1\n40\n5\nL-1\n2\n7\n4\nL-1\n8\n")
        salida = self.ejecutar_cli(entradas)
        self.assertIn("Precio base: S/ 40.00 | Cantidad: 7", salida)

    def test_demo_reproducible_y_mro(self) -> None:
        salida = self.ejecutar_cli("7\n3\n8\n")
        self.assertIn("Caso exitoso:", salida)
        self.assertIn("ValidationError controlado:", salida)
        self.assertIn("NotFoundError controlado:", salida)
        self.assertIn("MRO Libro: Libro -> Producto -> object", salida)
        self.assertIn("MRO Electronico: Electronico -> Producto -> object", salida)
        self.assertIn("El catálogo está vacío", salida)


if __name__ == "__main__":
    unittest.main()
