from Fecha import Fecha
class Cuenta:
  def __init__(self, id_temp, usuario, saldo, fecha_ultima_transaccion:Fecha, monto_retirado_ultimo_dia, monto_depositado_ultimo_dia):
    self.id_temp = id_temp
    self.usuario = usuario
    self.saldo = saldo
    
    fecha_actual = Fecha.hoy()
    if(fecha_ultima_transaccion.day != fecha_actual.day and 
       fecha_ultima_transaccion.month != fecha_actual.day and 
       fecha_ultima_transaccion.year != fecha_actual.day):
      self.monto_retirado_hoy = 0
      self.monto_depositado_hoy = 0
    else:
      self.monto_retirado_hoy = monto_retirado_ultimo_dia
      self.monto_depositado_hoy = monto_depositado_ultimo_dia
    self.fecha_ultima:Fecha = fecha_actual
    
  def __str__(self):
    return f"Cuenta : {self.user}\n Saldo : S/.({self.saldo})"

  def comprobar_nuevo_dia(self):
    fecha_actual = Fecha.hoy()
    if(self.fecha_ultima.day != fecha_actual.day and 
       self.fecha_ultima.day.month != fecha_actual.day and 
       self.fecha_ultima.day.year != fecha_actual.day):
      self.monto_depositado_hoy = 0
      self.monto_retirado_hoy = 0
      self.fecha_ultima:Fecha = fecha_actual
  
  def depositar(self, monto):
    self.saldo = self.saldo + monto
    self.monto_depositado_hoy = self.monto_depositado_hoy + monto

  def retirar(self, monto):
    self.saldo = self.saldo - monto
    self.monto_retirado_hoy = self.monto_retirado_hoy + monto

