import unittest
from datetime import datetime
from biblioteca import Libro, Revista, DVD

class TestBiblioteca(unittest.TestCase):
    def setUp(self):
        self.libro = Libro("L123", "El Gran Libro")
        self.revista = Revista("R456", "Revista de Ciencia")
        self.dvd = DVD("D789", "Película de Aventura")

    def mostrar_item(self, item):
        print(f'Título: {item.titulo}, Código: {item.codigo}, Fecha de devolución: {item.fecha_devolucion.strftime("%Y-%m-%d %H:%M:%S")}')
    
    def test_listado_biblioteca_items(self):
        print("Items prestados:")

        self.libro.prestar()
        self.mostrar_item(self.libro)
        
        self.revista.prestar()
        self.mostrar_item(self.revista)
        
        self.dvd.prestar()
        self.mostrar_item(self.dvd)


if __name__ == '__main__':
    unittest.main()
