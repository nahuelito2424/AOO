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
