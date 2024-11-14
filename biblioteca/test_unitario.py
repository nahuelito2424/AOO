from datetime import datetime, timedelta
from biblioteca import Libro, Revista, DVD 

class TestMaterialBiblioteca:

    def test_material_biblioteca(self):
        libro = Libro(codigo="L001", titulo="Libro de prueba")
        libro.prestar()
        print(f"Libro prestado después de llamar a prestar(): {libro.prestado}")
        print(f"Fecha de devolución libro: {libro.fecha_devolucion}\n")

        revista = Revista(codigo="R001", titulo="Revista de prueba")
        print(f"Revista prestada inicialmente: {revista.prestado}")
        revista.prestar()
        print(f"Fecha de devolución revista: {revista.fecha_devolucion}\n")

        dvd = DVD(codigo="D001", titulo="DVD de prueba")
        dvd.prestar()
        print(f"Fecha de devolución DVD: {dvd.fecha_devolucion}\n")

        prestamo_exitoso = libro.prestar()
        print(f"Intento de prestar el libro por segunda vez: {prestamo_exitoso}")

if __name__ == "__main__":
    pruebas = TestMaterialBiblioteca()
    pruebas.test_material_biblioteca()