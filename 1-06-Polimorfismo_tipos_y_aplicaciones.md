# Polimorfismo en Python: Implementación y Mejores Prácticas

## 1. Sistema de Procesamiento de Pagos

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol, List, Dict, Optional
from datetime import datetime

class ProcesadorPago(ABC):
    @abstractmethod
    def procesar(self, monto: Decimal, moneda: str) -> bool:
        """Procesa un pago con el monto y moneda especificados."""
        pass

    @abstractmethod
    def reembolsar(self, id_transaccion: str) -> bool:
        """Reembolsa una transacción específica."""
        pass

class ProcesadorTarjeta(ProcesadorPago):
    def __init__(self, proveedor: str):
        self.proveedor = proveedor
        self._transacciones: Dict[str, Decimal] = {}

    def procesar(self, monto: Decimal, moneda: str) -> bool:
        # Simulación de procesamiento con tarjeta
        id_transaccion = f"TX_{datetime.now().timestamp()}"
        self._transacciones[id_transaccion] = monto
        print(f"Procesando {monto} {moneda} con {self.proveedor}")
        return True

    def reembolsar(self, id_transaccion: str) -> bool:
        if id_transaccion in self._transacciones:
            monto = self._transacciones.pop(id_transaccion)
            print(f"Reembolsando {monto} via {self.proveedor}")
            return True
        return False

class ProcesadorPayPal(ProcesadorPago):
    def __init__(self, email_comercio: str):
        self.email_comercio = email_comercio
        self._transacciones: Dict[str, Dict] = {}

    def procesar(self, monto: Decimal, moneda: str) -> bool:
        id_transaccion = f"PP_{datetime.now().timestamp()}"
        self._transacciones[id_transaccion] = {
            'monto': monto,
            'moneda': moneda
        }
        print(f"Procesando {monto} {moneda} via PayPal")
        return True

    def reembolsar(self, id_transaccion: str) -> bool:
        if id_transaccion in self._transacciones:
            datos = self._transacciones.pop(id_transaccion)
            print(f"Reembolsando {datos['monto']} {datos['moneda']} via PayPal")
            return True
        return False

# Uso de polimorfismo paramétrico con genéricos
T = TypeVar('T')

class Resultado(Generic[T]):
    def __init__(self, valor: Optional[T] = None, error: Optional[str] = None):
        self.valor = valor
        self.error = error
        self.exitoso = error is None

@dataclass
class Transaccion:
    id: str
    monto: Decimal
    moneda: str
    fecha: datetime
    procesador: ProcesadorPago

class ServicioPagos:
    def __init__(self):
        self.procesadores: Dict[str, ProcesadorPago] = {}

    def agregar_procesador(self, nombre: str, procesador: ProcesadorPago) -> None:
        self.procesadores[nombre] = procesador

    def procesar_pago(
        self, 
        metodo: str, 
        monto: Decimal, 
        moneda: str = "USD"
    ) -> Resultado[Transaccion]:
        if metodo not in self.procesadores:
            return Resultado(error="Método de pago no soportado")

        procesador = self.procesadores[metodo]
        if procesador.procesar(monto, moneda):
            transaccion = Transaccion(
                id=f"{metodo}_{datetime.now().timestamp()}",
                monto=monto,
                moneda=moneda,
                fecha=datetime.now(),
                procesador=procesador
            )
            return Resultado(valor=transaccion)
        return Resultado(error="Error al procesar el pago")
```

## 2. Sistema de Formas Geométricas

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import math

class Forma(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimetro(self) -> float:
        pass

    def __add__(self, otra: 'Forma') -> float:
        """Sobrecarga del operador + para sumar áreas."""
        return self.area() + otra.area()

@dataclass
class Circulo(Forma):
    radio: float

    def area(self) -> float:
        return math.pi * self.radio ** 2

    def perimetro(self) -> float:
        return 2 * math.pi * self.radio

@dataclass
class Rectangulo(Forma):
    base: float
    altura: float

    def area(self) -> float:
        return self.base * self.altura

    def perimetro(self) -> float:
        return 2 * (self.base + self.altura)

    # Sobrecarga de operador * para escalar el rectángulo
    def __mul__(self, escala: float) -> 'Rectangulo':
        return Rectangulo(
            base=self.base * escala,
            altura=self.altura * escala
        )

class CalculadorFormas:
    def calcular_area_total(self, formas: List[Forma]) -> float:
        return sum(forma.area() for forma in formas)

    def ordenar_por_area(self, formas: List[Forma]) -> List[Forma]:
        return sorted(formas, key=lambda f: f.area())
```

## 3. Pruebas Unitarias

```python
import unittest
from decimal import Decimal

class TestProcesadorPagos(unittest.TestCase):
    def setUp(self):
        self.servicio = ServicioPagos()
        self.servicio.agregar_procesador(
            "tarjeta", 
            ProcesadorTarjeta("VISA")
        )
        self.servicio.agregar_procesador(
            "paypal", 
            ProcesadorPayPal("comercio@email.com")
        )

    def test_procesar_pago_tarjeta(self):
        resultado = self.servicio.procesar_pago(
            "tarjeta", 
            Decimal("100.00")
        )
        self.assertTrue(resultado.exitoso)
        self.assertIsNotNone(resultado.valor)
        self.assertEqual(resultado.valor.monto, Decimal("100.00"))

    def test_procesar_pago_metodo_invalido(self):
        resultado = self.servicio.procesar_pago(
            "bitcoin", 
            Decimal("100.00")
        )
        self.assertFalse(resultado.exitoso)
        self.assertEqual(
            resultado.error, 
            "Método de pago no soportado"
        )

class TestFormasGeometricas(unittest.TestCase):
    def test_suma_areas(self):
        circulo = Circulo(radio=2)
        rectangulo = Rectangulo(base=3, altura=4)
        area_total = circulo + rectangulo
        self.assertAlmostEqual(
            area_total, 
            math.pi * 4 + 12
        )

    def test_escalar_rectangulo(self):
        rectangulo = Rectangulo(base=2, altura=3)
        escalado = rectangulo * 2
        self.assertEqual(escalado.base, 4)
        self.assertEqual(escalado.altura, 6)
```

## 4. Mejores Prácticas

1. **Diseño**:
   - Usar interfaces abstractas para definir contratos
   - Implementar polimorfismo a través de herencia cuando sea apropiado
   - Aprovechar protocolos para interfaces implícitas

2. **Implementación**:
   - Mantener métodos polimórficos simples y cohesivos
   - Usar type hints para mejor documentación
   - Implementar operadores especiales cuando tenga sentido

3. **Testing**:
   - Probar todas las implementaciones polimórficas
   - Verificar comportamiento con diferentes tipos
   - Cubrir casos especiales y errores

## 5. Ejercicio Propuesto

Implementar un sistema de notificaciones que:
1. Soporte múltiples canales (email, SMS, push)
2. Permita formato personalizado por canal
3. Implemente priorización de mensajes
4. Use polimorfismo para manejar diferentes tipos de contenido

## Conclusión

El polimorfismo en Python ofrece flexibilidad y extensibilidad a través de diferentes mecanismos. La clave está en elegir el tipo adecuado de polimorfismo según las necesidades del sistema y mantener un diseño limpio y mantenible.