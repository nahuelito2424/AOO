# Abstracción en Programación Orientada a Objetos con Python

## 1. Conceptos Fundamentales

La abstracción es un pilar fundamental de la POO que nos permite:
- Simplificar sistemas complejos
- Reutilizar código eficientemente
- Crear diseños flexibles y escalables
- Mejorar la seguridad del código

## 2. Implementación en Python

### 2.1 Clases Abstractas

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre
    
    @abstractmethod
    def hacer_sonido(self) -> str:
        """Método que debe ser implementado por todas las subclases."""
        pass
    
    @abstractmethod
    def moverse(self) -> str:
        """Define cómo se mueve el animal."""
        pass

class Perro(Animal):
    def hacer_sonido(self) -> str:
        return "¡Guau!"
    
    def moverse(self) -> str:
        return "Caminando en cuatro patas"

class Pajaro(Animal):
    def hacer_sonido(self) -> str:
        return "¡Pío!"
    
    def moverse(self) -> str:
        return "Volando"
```

#### Diagrama de Clases

```mermaid
classDiagram
    class Animal {
        <<abstract>>
        +nombre: str
        +hacer_sonido(): str
        +moverse(): str
    }
    class Perro {
        +hacer_sonido(): str
        +moverse(): str
    }
    class Pajaro {
        +hacer_sonido(): str
        +moverse(): str
    }
    Animal <|-- Perro
    Animal <|-- Pajaro
```

### 2.2 Ejemplo Práctico: Sistema de Pagos

```python
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict

class MetodoPago(ABC):
    @abstractmethod
    def procesar_pago(self, monto: float) -> bool:
        pass
    
    @abstractmethod
    def verificar_fondos(self, monto: float) -> bool:
        pass

class TarjetaCredito(MetodoPago):
    def __init__(self, numero: str, fecha_vencimiento: str):
        self.numero = numero
        self.fecha_vencimiento = fecha_vencimiento
    
    def procesar_pago(self, monto: float) -> bool:
        if self.verificar_fondos(monto):
            print(f"Procesando pago de ${monto} con tarjeta {self.numero}")
            return True
        return False
    
    def verificar_fondos(self, monto: float) -> bool:
        # Simulación de verificación de fondos
        return True

class PayPal(MetodoPago):
    def __init__(self, email: str):
        self.email = email
    
    def procesar_pago(self, monto: float) -> bool:
        if self.verificar_fondos(monto):
            print(f"Procesando pago de ${monto} con PayPal ({self.email})")
            return True
        return False
    
    def verificar_fondos(self, monto: float) -> bool:
        # Simulación de verificación de fondos
        return True

class Transaccion:
    def __init__(self, metodo_pago: MetodoPago):
        self.metodo_pago = metodo_pago
        self.fecha = datetime.now()
    
    def ejecutar_pago(self, monto: float) -> bool:
        return self.metodo_pago.procesar_pago(monto)
```

#### Diagrama de Clases

```mermaid
classDiagram
    class MetodoPago {
        <<abstract>>
        +procesar_pago(monto: float): bool
        +verificar_fondos(monto: float): bool
    }
    class TarjetaCredito {
        -numero: str
        -fecha_vencimiento: str
        +procesar_pago(monto: float): bool
        +verificar_fondos(monto: float): bool
    }
    class PayPal {
        -email: str
        +procesar_pago(monto: float): bool
        +verificar_fondos(monto: float): bool
    }
    class Transaccion {	
        -metodo_pago: MetodoPago
        -fecha: datetime
        +ejecutar_pago(monto: float): bool
    }

    MetodoPago <|-- TarjetaCredito
    MetodoPago <|-- PayPal
    Transaccion o-- MetodoPago
```

### 2.3 Pruebas Unitarias

```python
import unittest
from datetime import datetime
from sistema_pagos import TarjetaCredito, PayPal, Transaccion

class TestMetodosPago(unittest.TestCase):
    def setUp(self):
        self.tarjeta = TarjetaCredito("1234-5678-9012-3456", "12/25")
        self.paypal = PayPal("hola@email.com")
        self.transacciones = []

    def realizar_pago_tarjeta(self, monto: float):
        transaccion = Transaccion(self.tarjeta)
        transaccion.ejecutar_pago(monto)
        self.transacciones.append(transaccion)

    def realizar_pago_paypal(self, monto: float):
        transaccion = Transaccion(self.paypal)
        transaccion.ejecutar_pago(monto)
        self.transacciones.append(transaccion)

    def test_pago(self):
        self.realizar_pago_tarjeta(100.0)
        self.realizar_pago_paypal(50.0)
        self.realizar_pago_tarjeta(200.0)
        for transaccion in self.transacciones:
            print(f'Método de pago: {transaccion.metodo_pago.__class__.__name__}, Fecha: {transaccion.fecha.strftime("%Y-%m-%d %H:%M:%S")}')

if __name__ == '__main__':
    unittest.main()
```

## Output pruebas unitarias
```text
Procesando pago de $100.0 con tarjeta 1234-5678-9012-3456
Procesando pago de $50.0 con PayPal (hola@email.com)      
Procesando pago de $200.0 con tarjeta 1234-5678-9012-3456 
Método de pago: TarjetaCredito, Fecha: 2024-11-14 20:06:30
Método de pago: PayPal, Fecha: 2024-11-14 20:06:30        
Método de pago: TarjetaCredito, Fecha: 2024-11-14 20:06:30
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```

## 3. Ejercicio Práctico: Sistema de Biblioteca

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime, timedelta

class MaterialBiblioteca(ABC):
    def __init__(self, codigo: str, titulo: str):
        self.codigo = codigo
        self.titulo = titulo
        self.prestado = False
        self.fecha_devolucion: Optional[datetime] = None
    
    @abstractmethod
    def calcular_fecha_devolucion(self) -> datetime:
        pass
    
    def prestar(self) -> bool:
        if not self.prestado:
            self.prestado = True
            self.fecha_devolucion = self.calcular_fecha_devolucion()
            return True
        return False

class Libro(MaterialBiblioteca):
    def calcular_fecha_devolucion(self) -> datetime:
        return datetime.now() + timedelta(days=14)

class Revista(MaterialBiblioteca):
    def calcular_fecha_devolucion(self) -> datetime:
        return datetime.now() + timedelta(days=7)

class DVD(MaterialBiblioteca):
    def calcular_fecha_devolucion(self) -> datetime:
        return datetime.now() + timedelta(days=3)
```

### Diagrama de clases
```mermaid
classDiagram
    class MaterialBiblioteca {
        +str codigo
        +str titulo
        +bool prestado
        +datetime fecha_devolucion
        +prestar() bool
        <<abstract>>
        +calcular_fecha_devolucion() datetime
    }

    class Libro {
        +calcular_fecha_devolucion() datetime
    }

    class Revista {
        +calcular_fecha_devolucion() datetime
    }

    class DVD {
        +calcular_fecha_devolucion() datetime
    }

    MaterialBiblioteca <|-- Libro
    MaterialBiblioteca <|-- Revista
    MaterialBiblioteca <|-- DVD
```


### Diagrama de secuencia
```mermaid
sequenceDiagram
    participant Biblioteca
    participant MaterialBiblioteca

    Biblioteca->>MaterialBiblioteca: Llamada a prestar()
    MaterialBiblioteca->>MaterialBiblioteca: Verifica si está prestado
    MaterialBiblioteca->>MaterialBiblioteca: Llama a calcular_fecha_devolucion()
    MaterialBiblioteca->>Biblioteca: Retorna la fecha de devolución
    Biblioteca->>Biblioteca: Asigna fecha de devolución
```


### Pruebas Unitarias
```python
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
```
## Output pruebas unitarias 
```text
Items prestados:
Título: El Gran Libro, Código: L123, Fecha de devolución: 2024-11-28 20:16:12
Título: Revista de Ciencia, Código: R456, Fecha de devolución: 2024-11-21 20:16:12
Título: Película de Aventura, Código: D789, Fecha de devolución: 2024-11-17 20:16:12
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```



## 4. Mejores Prácticas

1. **Diseño**:
   - Usar clases abstractas para definir interfaces comunes
   - Mantener la abstracción en el nivel adecuado
   - Separar responsabilidades claramente

2. **Implementación**:
   - Utilizar type hints para mejor documentación
   - Implementar métodos abstractos en todas las subclases
   - Mantener la cohesión alta y el acoplamiento bajo

3. **Testing**:
   - Probar cada implementación concreta
   - Verificar el comportamiento polimórfico
   - Cubrir casos especiales y errores

## 5. Ejercicios Propuestos

1. Implementar un sistema de notificaciones con diferentes medios (email, SMS, push)
2. Crear un simulador de vehículos con distintos tipos de transporte
3. Diseñar un sistema de procesamiento de archivos para diferentes formatos

## Conclusión

La abstracción en Python permite crear sistemas flexibles y mantenibles. La clave está en identificar las características comunes y modelarlas de manera que permitan extensibilidad y reutilización del código.