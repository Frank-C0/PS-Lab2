import json
from Cuenta import Cuenta
from Fecha import Fecha


class DBCuentas:
  def __init__(self, json_reader):
    self.json_reader = json_reader
    self.db = json.load(self.json_reader)

  def get_cuenta(self, username, password):
    

    cont_id = 0
    for user in self.db['users']:
      if str(user['username']) == str(username):
        if str(user['password']) == str(password):
          fecha_ultima = user['fecha_ultima_transaccion']
          return Cuenta(
            cont_id,
            user['username'],
            user['saldo'],
            Fecha(fecha_ultima['day'],fecha_ultima['month'],fecha_ultima['year']),
            user['monto_retirado_ultimo_dia'],
            user['monto_depositado_ultimo_dia']
          )
    cont_id = cont_id + 1
    
    return None

    