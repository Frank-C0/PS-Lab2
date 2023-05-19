import unittest
from DataBaseJSONCuentas import DBCuentas
import io

from Fecha import Fecha

class TestDBJSON(unittest.TestCase):

  def setUp(self):
    self.fecha_actual = Fecha.hoy()
    self.db_cuentas = DBCuentas(io.StringIO('''
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
    ''' % (self.fecha_actual.day, self.fecha_actual.month, self.fecha_actual.year)))
    
  def test_get_user(self):
    cuenta = self.db_cuentas.get_cuenta('Frank', '12345')
    
    self.assertNotEqual(cuenta, None)
    self.assertEqual(cuenta.usuario, 'Frank')
    self.assertEqual(cuenta.saldo, 5000)
    self.assertEqual(cuenta.fecha_ultima.day, self.fecha_actual.day)
    self.assertEqual(cuenta.fecha_ultima.month, self.fecha_actual.month)
    self.assertEqual(cuenta.fecha_ultima.year, self.fecha_actual.year)
    self.assertEqual(cuenta.monto_retirado_hoy, 500)
    self.assertEqual(cuenta.monto_depositado_hoy, 500)
    
    
  def test_get_non_existent_user(self):
    cuenta = self.db_cuentas.get_cuenta('NNNNN', '00000')
    self.assertEqual(cuenta, None)
    
    cuenta = self.db_cuentas.get_cuenta('Frank', '00000')
    self.assertEqual(cuenta, None)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestDBJSON)
  unittest.TextTestRunner(verbosity=2).run(suite)
