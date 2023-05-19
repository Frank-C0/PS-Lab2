import numbers
import os
from Cuenta import Cuenta
from DataBaseJSONCuentas import DBCuentas

def isNumber(num):
  return isinstance(num, numbers.Number)
  
class MONTO_NO_NUMERICO(Exception):
  pass
class MONTO_NEGATIVO(Exception):
  pass
class ERROR_NO_HAY_CUENTA_SELECCIONADA(Exception):
  pass
class LIMITE_DE_RETIRO_DIARIO_EXCEDIDO(Exception):
  pass
class LIMITE_DE_DEPOSITO_DIARIO_EXCEDIDO(Exception):
  pass
class ERROR_MINIMO_DE_DEPOSITO(Exception):
  pass
class ERROR_MINIMO_DE_RETIRO(Exception):
  pass
class SALDO_INSUFICIENTE(Exception):
  pass
class MAX_LOGIN_INTENTOS(Exception):
  pass

class Cajero:
  MAX_INTENTOS_LOGIN = 3
  MAX_RETIRO_DIARIO = 3000
  MIN_RETIRO_DIARIO = 0
  MAX_DEPOSITO_DIARIO = 3000
  MIN_DEPOSITO_DIARIO = 0

  def __init__(self, reader_file_db_json):
    self.db_cuentas = DBCuentas(reader_file_db_json)
    self.current_account:Cuenta = None
    self.login_intentos = 0
    
  def login_user(self, username, password):
    self.login_intentos = self.login_intentos + 1
    user = self.db_cuentas.get_cuenta(username, password)

    if user != None:
      self.current_account = user
      self.login_intentos = 0
    else:
      if self.login_intentos == Cajero.MAX_INTENTOS_LOGIN:
        raise MAX_LOGIN_INTENTOS()
    return Cajero.MAX_INTENTOS_LOGIN - self.login_intentos

  def deposito(self, monto):
    self.current_account.comprobar_nuevo_dia()

    if not isNumber(monto):
      raise MONTO_NO_NUMERICO()
    if monto < 0:
      raise MONTO_NEGATIVO()
    if monto < Cajero.MIN_DEPOSITO_DIARIO:
      raise ERROR_MINIMO_DE_DEPOSITO
    if self.current_account.monto_depositado_hoy + monto > Cajero.MAX_RETIRO_DIARIO:
      raise LIMITE_DE_DEPOSITO_DIARIO_EXCEDIDO
    
    self.current_account.depositar(monto)
    
  def retiro(self, monto):
    self.current_account.comprobar_nuevo_dia()

    if not isNumber(monto):
      raise MONTO_NO_NUMERICO()
    if monto < 0:
      raise MONTO_NEGATIVO()
    if monto < Cajero.MIN_RETIRO_DIARIO:
      raise ERROR_MINIMO_DE_DEPOSITO
    if monto > self.current_account.saldo:
      raise SALDO_INSUFICIENTE()
    if self.current_account.monto_retirado_hoy + monto > Cajero.MAX_RETIRO_DIARIO:
      raise LIMITE_DE_RETIRO_DIARIO_EXCEDIDO
    
    self.current_account.retirar(monto)
    
  def get_saldo(self):
    return self.current_account.saldo
  

class MenuCajero:
  def __init__(self):
    self.continuar_menu = True
    self.cajero:Cajero = Cajero(open('datos.json'))
    
  def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

  def menu_opciones(self):
    print(""" Bienvenido al cajero automatico

            ******Menú******
            0- Ingresar con otro usuario

            1- Depositar

            2- Retirar

            3- Ver saldo

            4- Salir """)

    opcion = input("Su opción es: ")

    if opcion == "1":
      self.depositar_opcion()
    elif opcion == "2":
      self.retirar_opcion()
    elif opcion == "3":
      self.ver_saldo()
    elif opcion == "4":
      print("Programa finalizado")
    elif opcion == "0":
      self.login_opcion()
    else:
      print("NO existe esa opción")
      
  def start_menu(self):
    MenuCajero.clear_console()  # multi sistema operativo
    self.login_opcion()

    while self.continuar_menu:
      MenuCajero.clear_console()
      self.menu_opciones()

  def login_opcion(self):
    self.cajero.current_account = None # borrar cuenta seleccionada antes
    try:
      while True:
        username = input("Ingrese su nombre de usuario: ")
        password = input("Ingrese su contraseña: ")
        intentos = self.cajero.login_user(username, password)

        if self.cajero.current_account == None:
          print(f"\nUsuario o contraseña incorrecta, le quedan {intentos} intentos")
        else:
          print('Cuenta correcta')
          break

    except MAX_LOGIN_INTENTOS:
      print('Ha alcanzado el maximo de intentos. No puede realizar operaciones.')
    
  def depositar_opcion(self):
    entrada = input("Ingrese su monto a depositar:")
    
    try:
      monto = int(entrada)
    except ValueError:
      print('Ingrese un monto moneratio valido')

    try:
      self.cajero.deposito(monto)

      print("Usted a depositado", monto)
      print(f"Su nuevo saldo es {self.cajero.get_saldo()}")
    except MONTO_NO_NUMERICO:
      print('Ingrese un monto valido')
    except MONTO_NEGATIVO:
      print('Ingrese un monto positivo')
    except ERROR_MINIMO_DE_DEPOSITO:
      print('El monto ingresado no alcanza el minimo de deposito')
    except LIMITE_DE_DEPOSITO_DIARIO_EXCEDIDO:
      print(f"El monto excede el maximo de deposito diario de {Cajero.MAX_DEPOSITO_DIARIO}")
    finally:
      MenuCajero.enter_to_confirm()
  def retirar_opcion(self):
    monto = input("¿Cuánto desea retirar? : ")
    print(monto)
    print(type(monto))
    try:
      monto = int(monto)
      print(monto)
      print(type(monto))
    except ValueError:
      print('Ingrese un monto moneratio valido')
            
    print("Su saldo era de ", self.cajero.get_saldo())

    try:
      self.cajero.retiro(monto)
      
      print(f"Usted a retirado: {monto}\nSu nuevo saldo es {self.cajero.get_saldo()}")
      
    except MONTO_NO_NUMERICO:
      print('Ingrese un monto valido')
    except MONTO_NEGATIVO:
      print('Ingrese un monto positivo')
    except ERROR_MINIMO_DE_RETIRO:
      print('No cuenta con fondos suficientes para retirar el monto')
    except LIMITE_DE_RETIRO_DIARIO_EXCEDIDO:
      print(f"El monto excede el maximo de retiro diario de {Cajero.MAX_DEPOSITO_DIARIO}")
    finally:
      MenuCajero.enter_to_confirm()

  def ver_saldo(self):
    MenuCajero.clear_console()
    print("Su saldo es: ", self.cajero.get_saldo())
    MenuCajero.enter_to_confirm()

  def salir(self):
    self.continuar_menu = False

  def enter_to_confirm():
    input('\nPresione ENTER para continuar al menu\n')


