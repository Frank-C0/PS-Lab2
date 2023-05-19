import datetime

class Fecha:
  def __init__(self, day, month, year):
    self.day = day
    self.month = month
    self.year = year

  def hoy():
    fecha_actual = datetime.datetime.now()
    return Fecha(fecha_actual.day, fecha_actual.month, fecha_actual.year)
  
  