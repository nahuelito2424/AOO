# Modularidad en Python: Diseño y Aplicación Práctica

## 1. Fundamentos de la Modularidad

La modularidad en Python se implementa mediante:
- Módulos (archivos .py)
- Paquetes (directorios con __init__.py)
- Clases y funciones bien organizadas
- Interfaces claras entre componentes

## 2. Implementación Práctica: Sistema de E-commerce

### 2.1 Estructura del Proyecto
```
ecommerce/
│
├── __init__.py
├── producto/
│   ├── __init__.py
│   ├── modelo.py
│   └── repositorio.py
│
├── pedido/
│   ├── __init__.py
│   ├── modelo.py
│   └── servicio.py
│
└── pago/
    ├── __init__.py
    ├── procesador.py
    └── proveedor/
        ├── __init__.py
        ├── paypal.py
        └── stripe.py
```

### 2.2 Implementación de Módulos

```python
# producto/modelo.py
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class Producto:
    id: int
    nombre: str
    precio: Decimal
    stock: int
    descripcion: Optional[str] = None

# producto/repositorio.py
from typing import List, Optional
from .modelo import Producto

class ProductoRepositorio:
    def __init__(self):
        self._productos: List[Producto] = []

    def agregar(self, producto: Producto) -> None:
        self._productos.append(producto)

    def buscar_por_id(self, id: int) -> Optional[Producto]:
        return next((p for p in self._productos if p.id == id), None)

    def actualizar_stock(self, id: int, cantidad: int) -> bool:
        producto = self.buscar_por_id(id)
        if producto and producto.stock >= cantidad:
            producto.stock -= cantidad
            return True
        return False

# pedido/modelo.py
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List
from ..producto.modelo import Producto

@dataclass
class LineaPedido:
    producto: Producto
    cantidad: int
    precio_unitario: Decimal

    @property
    def subtotal(self) -> Decimal:
        return self.precio_unitario * self.cantidad

@dataclass
class Pedido:
    id: int
    fecha: datetime
    lineas: List[LineaPedido]
    estado: str = "pendiente"

    @property
    def total(self) -> Decimal:
        return sum(linea.subtotal for linea in self.lineas)

# pago/procesador.py
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict

class ProcesadorPago(ABC):
    @abstractmethod
    def procesar(self, monto: Decimal, datos: Dict) -> bool:
        pass

# pago/proveedor/paypal.py
from ..procesador import ProcesadorPago
from decimal import Decimal
from typing import Dict

class PayPalProcesador(ProcesadorPago):
    def procesar(self, monto: Decimal, datos: Dict) -> bool:
        # Implementación de procesamiento PayPal
        print(f"Procesando ${monto} con PayPal")
        return True

# Uso del sistema
class ServicioPedidos:
    def __init__(
        self,
        repo_productos: ProductoRepositorio,
        procesador_pago: ProcesadorPago
    ):
        self.repo_productos = repo_productos
        self.procesador_pago = procesador_pago
        self._pedidos: List[Pedido] = []

    def crear_pedido(
        self, 
        items: List[tuple[int, int]], 
        datos_pago: Dict
    ) -> Optional[Pedido]:
        lineas_pedido = []
        
        # Verificar stock y crear líneas de pedido
        for producto_id, cantidad in items:
            producto = self.repo_productos.buscar_por_id(producto_id)
            if not producto or not self.repo_productos.actualizar_stock(
                producto_id, 
                cantidad
            ):
                return None
                
            lineas_pedido.append(
                LineaPedido(producto, cantidad, producto.precio)
            )

        # Crear pedido
        pedido = Pedido(
            id=len(self._pedidos) + 1,
            fecha=datetime.now(),
            lineas=lineas_pedido
        )

        # Procesar pago
        if self.procesador_pago.procesar(pedido.total, datos_pago):
            self._pedidos.append(pedido)
            return pedido
        return None
```

## 3. Pruebas Unitarias

```python
import unittest
from decimal import Decimal
from ecommerce.producto.modelo import Producto
from ecommerce.producto.repositorio import ProductoRepositorio
from ecommerce.pago.proveedor.paypal import PayPalProcesador
from ecommerce.pedido.servicio import ServicioPedidos

class TestSistemaEcommerce(unittest.TestCase):
    def setUp(self):
        self.repo = ProductoRepositorio()
        self.procesador = PayPalProcesador()
        self.servicio = ServicioPedidos(self.repo, self.procesador)
        
        # Agregar productos de prueba
        self.repo.agregar(Producto(1, "Laptop", Decimal("999.99"), 10))
        self.repo.agregar(Producto(2, "Mouse", Decimal("29.99"), 20))

    def test_crear_pedido_exitoso(self):
        items = [(1, 1), (2, 2)]  # 1 laptop, 2 mouse
        datos_pago = {"email": "cliente@email.com"}
        
        pedido = self.servicio.crear_pedido(items, datos_pago)
        
        self.assertIsNotNone(pedido)
        self.assertEqual(len(pedido.lineas), 2)
        self.assertEqual(pedido.total, Decimal("1059.97"))

    def test_crear_pedido_sin_stock(self):
        items = [(1, 11)]  # Intentar comprar más laptops que el stock
        datos_pago = {"email": "cliente@email.com"}
        
        pedido = self.servicio.crear_pedido(items, datos_pago)
        
        self.assertIsNone(pedido)

if __name__ == '__main__':
    unittest.main()
```

## 4. Mejores Prácticas

1. **Organización**:
   - Un módulo por archivo
   - Nombres descriptivos y consistentes
   - Separación clara de responsabilidades

2. **Diseño**:
   - Usar inyección de dependencias
   - Definir interfaces claras
   - Minimizar acoplamiento entre módulos

3. **Importaciones**:
   - Evitar importaciones circulares
   - Usar importaciones absolutas
   - Mantener __init__.py limpios

## 5. Ejercicio Práctico

Implementar un sistema de gestión de inventario con los siguientes módulos:
1. Gestión de productos
2. Control de stock
3. Generación de reportes
4. Alertas de bajo stock

## Conclusión

La modularidad en Python permite crear sistemas escalables y mantenibles. La clave está en una buena organización del código y la definición clara de responsabilidades e interfaces entre módulos.