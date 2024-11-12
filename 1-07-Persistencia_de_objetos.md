# Persistencia de Objetos en Python

## 1. Sistema de Gestión de Biblioteca con SQLAlchemy

```python
from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Decimal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session, sessionmaker

# Configuración Base
Base = declarative_base()
engine = create_engine('sqlite:///biblioteca.db')

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.now)
    prestamos = relationship("Prestamo", back_populates="usuario")
    
    def __repr__(self):
        return f"Usuario(id={self.id}, nombre='{self.nombre}')"

class Libro(Base):
    __tablename__ = 'libros'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(100))
    isbn = Column(String(13), unique=True)
    copias_disponibles = Column(Integer, default=1)
    prestamos = relationship("Prestamo", back_populates="libro")
    
    def __repr__(self):
        return f"Libro(titulo='{self.titulo}', autor='{self.autor}')"

class Prestamo(Base):
    __tablename__ = 'prestamos'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    libro_id = Column(Integer, ForeignKey('libros.id'))
    fecha_prestamo = Column(DateTime, default=datetime.now)
    fecha_devolucion = Column(DateTime, nullable=True)
    
    usuario = relationship("Usuario", back_populates="prestamos")
    libro = relationship("Libro", back_populates="prestamos")
    
    def __repr__(self):
        return f"Prestamo(usuario='{self.usuario.nombre}', libro='{self.libro.titulo}')"

# Servicio de Biblioteca
class ServicioBiblioteca:
    def __init__(self, session: Session):
        self.session = session
    
    def registrar_usuario(self, nombre: str, email: str) -> Usuario:
        usuario = Usuario(nombre=nombre, email=email)
        self.session.add(usuario)
        self.session.commit()
        return usuario
    
    def agregar_libro(
        self, 
        titulo: str, 
        autor: str, 
        isbn: str, 
        copias: int = 1
    ) -> Libro:
        libro = Libro(
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            copias_disponibles=copias
        )
        self.session.add(libro)
        self.session.commit()
        return libro
    
    def prestar_libro(self, usuario_id: int, libro_id: int) -> Optional[Prestamo]:
        libro = self.session.query(Libro).get(libro_id)
        if not libro or libro.copias_disponibles <= 0:
            return None
            
        prestamo = Prestamo(
            usuario_id=usuario_id,
            libro_id=libro_id
        )
        libro.copias_disponibles -= 1
        
        self.session.add(prestamo)
        self.session.commit()
        return prestamo
    
    def devolver_libro(self, prestamo_id: int) -> bool:
        prestamo = self.session.query(Prestamo).get(prestamo_id)
        if not prestamo or prestamo.fecha_devolucion:
            return False
            
        prestamo.fecha_devolucion = datetime.now()
        prestamo.libro.copias_disponibles += 1
        self.session.commit()
        return True
```

## 2. Serialización con JSON y Archivos

```python
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime, date
from pathlib import Path

@dataclass
class Nota:
    titulo: str
    contenido: str
    fecha_creacion: date
    etiquetas: List[str]
    id: Optional[int] = None

class GestorNotas:
    def __init__(self, archivo: str):
        self.archivo = Path(archivo)
        self.notas: Dict[int, Nota] = {}
        self._cargar_notas()
    
    def _cargar_notas(self) -> None:
        if not self.archivo.exists():
            return
            
        try:
            with open(self.archivo, 'r') as f:
                notas_dict = json.load(f)
                for nota_dict in notas_dict:
                    nota_dict['fecha_creacion'] = date.fromisoformat(
                        nota_dict['fecha_creacion']
                    )
                    nota = Nota(**nota_dict)
                    self.notas[nota.id] = nota
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error al cargar notas: {e}")
    
    def _guardar_notas(self) -> None:
        notas_list = [asdict(nota) for nota in self.notas.values()]
        for nota_dict in notas_list:
            nota_dict['fecha_creacion'] = nota_dict['fecha_creacion'].isoformat()
            
        with open(self.archivo, 'w') as f:
            json.dump(notas_list, f, indent=2)
    
    def crear_nota(
        self, 
        titulo: str, 
        contenido: str, 
        etiquetas: List[str] = []
    ) -> Nota:
        nuevo_id = max(self.notas.keys(), default=0) + 1
        nota = Nota(
            id=nuevo_id,
            titulo=titulo,
            contenido=contenido,
            fecha_creacion=date.today(),
            etiquetas=etiquetas
        )
        self.notas[nuevo_id] = nota
        self._guardar_notas()
        return nota
    
    def actualizar_nota(
        self, 
        id: int, 
        titulo: Optional[str] = None,
        contenido: Optional[str] = None,
        etiquetas: Optional[List[str]] = None
    ) -> Optional[Nota]:
        if id not in self.notas:
            return None
            
        nota = self.notas[id]
        if titulo:
            nota.titulo = titulo
        if contenido:
            nota.contenido = contenido
        if etiquetas is not None:
            nota.etiquetas = etiquetas
            
        self._guardar_notas()
        return nota
    
    def eliminar_nota(self, id: int) -> bool:
        if id not in self.notas:
            return False
            
        del self.notas[id]
        self._guardar_notas()
        return True
    
    def buscar_por_etiqueta(self, etiqueta: str) -> List[Nota]:
        return [
            nota for nota in self.notas.values() 
            if etiqueta in nota.etiquetas
        ]
```

## 3. Pruebas Unitarias

```python
import unittest
from pathlib import Path
import tempfile
import os

class TestGestorNotas(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.archivo_notas = Path(self.temp_dir) / "notas.json"
        self.gestor = GestorNotas(str(self.archivo_notas))
    
    def tearDown(self):
        if self.archivo_notas.exists():
            os.remove(self.archivo_notas)
        os.rmdir(self.temp_dir)
    
    def test_crear_nota(self):
        nota = self.gestor.crear_nota(
            "Prueba", 
            "Contenido", 
            ["test"]
        )
        self.assertEqual(nota.titulo, "Prueba")
        self.assertEqual(nota.id, 1)
        
        # Verificar persistencia
        gestor2 = GestorNotas(str(self.archivo_notas))
        nota_cargada = gestor2.notas.get(1)
        self.assertIsNotNone(nota_cargada)
        self.assertEqual(nota_cargada.titulo, "Prueba")
    
    def test_actualizar_nota(self):
        nota = self.gestor.crear_nota("Original", "Contenido")
        nota_actualizada = self.gestor.actualizar_nota(
            nota.id,
            titulo="Modificado"
        )
        self.assertEqual(nota_actualizada.titulo, "Modificado")
        
        # Verificar persistencia
        gestor2 = GestorNotas(str(self.archivo_notas))
        self.assertEqual(
            gestor2.notas[nota.id].titulo,
            "Modificado"
        )

class TestServicioBiblioteca(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.servicio = ServicioBiblioteca(self.session)
    
    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(engine)
    
    def test_prestar_libro(self):
        usuario = self.servicio.registrar_usuario(
            "Ana",
            "ana@test.com"
        )
        libro = self.servicio.agregar_libro(
            "Python",
            "Guido",
            "123-456",
            2
        )
        
        prestamo = self.servicio.prestar_libro(
            usuario.id,
            libro.id
        )
        self.assertIsNotNone(prestamo)
        self.assertEqual(libro.copias_disponibles, 1)
```

## 4. Mejores Prácticas

1. **ORM**:
   - Usar sesiones de manera segura
   - Implementar relaciones adecuadamente
   - Manejar transacciones correctamente

2. **Serialización**:
   - Validar datos al deserializar
   - Manejar tipos de datos especiales
   - Implementar manejo de errores

3. **General**:
   - Separar lógica de negocio de persistencia
   - Usar type hints para claridad
   - Implementar pruebas exhaustivas

## 5. Ejercicio Propuesto

Implementar un sistema de gestión de tareas que:
1. Use SQLAlchemy para persistencia
2. Soporte exportación/importación JSON
3. Implemente búsqueda y filtrado
4. Maneje relaciones entre tareas

## Conclusión

La persistencia de objetos en Python puede implementarse eficientemente usando diferentes estrategias según las necesidades. La clave está en elegir el método adecuado y seguir las mejores prácticas de diseño.