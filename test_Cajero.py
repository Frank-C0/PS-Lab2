import io
import unittest
import Cajero
from Fecha import Fecha

class TestCajero(unittest.TestCase):

  def setUp(self):
    fecha_actual = Fecha.hoy()
    self.cajero = Cajero.Cajero(io.StringIO('''
{
    "users": [
      {
        "username": "Frank",
        "password": 12345,
        "saldo": 5000,
        "fecha_ultima_transaccion": {
          "day": %d, 
          "month": %d, 
          "year": %d 
        },
        "monto_retirado_ultimo_dia": 500,
        "monto_depositado_ultimo_dia": 500
      }
    ]
  }
    ''' % (fecha_actual.day, fecha_actual.month, fecha_actual.year)))

    self.cajero.login_user('Frank', '12345')

  def test_limite_de_login(self):
    self.cajero.login_user('','') #1
    self.cajero.login_user('','') #2

    self.assertRaises(Cajero.MAX_LOGIN_INTENTOS, self.cajero.login_user, '','') #3

  def test_deposito_normal(self):
    saldo_inicial = self.cajero.get_saldo()
    monto_a_depositar = 100
    
    self.cajero.deposito(monto_a_depositar)
    self.assertEqual(self.cajero.get_saldo(), saldo_inicial+monto_a_depositar)
  
  def test_deposito_limitado(self):
    saldo_inicial = self.cajero.get_saldo()
    monto_a_depositar = 2000
    self.cajero.deposito(monto_a_depositar)
    self.assertEqual(self.cajero.get_saldo(), saldo_inicial+monto_a_depositar)
    
    monto_a_depositar = 2000
    self.assertRaises(Cajero.LIMITE_DE_DEPOSITO_DIARIO_EXCEDIDO, self.cajero.deposito, monto_a_depositar)
    self.assertEqual(self.cajero.get_saldo(), self.cajero.get_saldo())

  def test_deposito_limitado_valor_inicial(self):
    # la cuenta usada se creó con 500 de monto depositado el dia de hoy
    monto_a_depositar = 2600
    
    self.assertRaises(Cajero.LIMITE_DE_DEPOSITO_DIARIO_EXCEDIDO, self.cajero.deposito, monto_a_depositar)
    self.assertEqual(self.cajero.get_saldo(), self.cajero.get_saldo())

  def test_deposito_incorrecto(self):
    self.assertRaises(Cajero.MONTO_NO_NUMERICO, self.cajero.deposito, 'mil')

  def test_deposito_negativo(self):
    self.assertRaises(Cajero.MONTO_NEGATIVO, self.cajero.deposito, -100)

  def test_retiro_normal(self):
    saldo_inicial = self.cajero.get_saldo()
    monto_a_retirar = 100
    
    self.cajero.retiro(monto_a_retirar)
    self.assertEqual(self.cajero.get_saldo(), saldo_inicial-monto_a_retirar)
  
  def test_retiro_limitado(self):
    saldo_inicial = self.cajero.get_saldo()
    monto_a_retirar = 2000
    self.cajero.retiro(monto_a_retirar)
    self.assertEqual(self.cajero.get_saldo(), saldo_inicial-monto_a_retirar)
    
    saldo_inicial = self.cajero.get_saldo()
    monto_a_retirar = 2000
    
    self.assertRaises(Cajero.LIMITE_DE_RETIRO_DIARIO_EXCEDIDO, self.cajero.retiro, monto_a_retirar)
    self.assertEqual(self.cajero.get_saldo(), self.cajero.get_saldo())

  def test_retiro_limitado_valor_inicial(self):
    # la cuenta usada se creó con 500 de monto retirado el dia de hoy
    monto_a_depositar = 2600
    
    self.assertRaises(Cajero.LIMITE_DE_RETIRO_DIARIO_EXCEDIDO, self.cajero.retiro, monto_a_depositar)
    self.assertEqual(self.cajero.get_saldo(), self.cajero.get_saldo())

  def test_retiro_incorrecto(self):
    self.assertRaises(Cajero.MONTO_NO_NUMERICO, self.cajero.retiro, 'mil')

  def test_retiro_negativo(self):
    self.assertRaises(Cajero.MONTO_NEGATIVO, self.cajero.retiro, -100)

  def test_retiro_saldo_insuficiente(self):    
    self.assertRaises(Cajero.SALDO_INSUFICIENTE, self.cajero.retiro,100000)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCajero)
  unittest.TextTestRunner(verbosity=2).run(suite)

  