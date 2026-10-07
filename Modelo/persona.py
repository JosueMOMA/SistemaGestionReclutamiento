# Modelo/persona.py
import re
from datetime import date

from Modelo.excepciones import DatoInvalidoError
from Modelo.validaciones import validar_digitos, validar_fecha, validar_texto


class Persona:
  """Clase padre con los datos personales. Postulante hereda de ella (Unidad 2)."""

  def __init__(
      self,
      dni,
      apellido_paterno,
      apellido_materno,
      nombres,
      sexo,
      estado_civil,
      fecha_nacimiento,
      celular,
      correo_electronico,
      departamento,
      provincia,
      distrito,
      direccion,
  ):
    # Se asigna mediante las properties para que cada dato pase por su validación.
    self.dni = dni
    self.apellido_paterno = apellido_paterno
    self.apellido_materno = apellido_materno
    self.nombres = nombres
    self.sexo = sexo
    self.estado_civil = estado_civil
    self.fecha_nacimiento = fecha_nacimiento
    self.celular = celular
    self.correo_electronico = correo_electronico
    self.departamento = departamento
    self.provincia = provincia
    self.distrito = distrito
    self.direccion = direccion

  # ---------- Properties ----------
  @property
  def dni(self):
    return self.__dni

  @dni.setter
  def dni(self, valor):
    self.__dni = validar_digitos(valor, "DNI", 8)

  @property
  def apellido_paterno(self):
    return self.__apellido_paterno

  @apellido_paterno.setter
  def apellido_paterno(self, valor):
    self.__apellido_paterno = validar_texto(valor, "Apellido Paterno")

  @property
  def apellido_materno(self):
    return self.__apellido_materno

  @apellido_materno.setter
  def apellido_materno(self, valor):
    self.__apellido_materno = validar_texto(valor, "Apellido Materno")

  @property
  def nombres(self):
    return self.__nombres

  @nombres.setter
  def nombres(self, valor):
    self.__nombres = validar_texto(valor, "Nombres")

  @property
  def sexo(self):
    return self.__sexo

  @sexo.setter
  def sexo(self, valor):
    self.__sexo = validar_texto(valor, "Sexo")

  @property
  def estado_civil(self):
    return self.__estado_civil

  @estado_civil.setter
  def estado_civil(self, valor):
    self.__estado_civil = validar_texto(valor, "Estado Civil")

  @property
  def fecha_nacimiento(self):
    return self.__fecha_nacimiento

  @fecha_nacimiento.setter
  def fecha_nacimiento(self, valor):
    fecha = validar_fecha(valor, "Fecha de Nacimiento")
    if fecha > date.today():
      raise DatoInvalidoError("La fecha de nacimiento no puede ser futura.")
    self.__fecha_nacimiento = fecha

  @property
  def celular(self):
    return self.__celular

  @celular.setter
  def celular(self, valor):
    texto = validar_digitos(valor, "Celular", 9)
    if not texto.startswith("9"):
      raise DatoInvalidoError("El celular debe empezar con 9.")
    self.__celular = texto

  @property
  def correo_electronico(self):
    return self.__correo_electronico

  @correo_electronico.setter
  def correo_electronico(self, valor):
    texto = validar_texto(valor, "Correo Electrónico")
    if not re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", texto):
      raise DatoInvalidoError("El correo electrónico no tiene un formato válido.")
    self.__correo_electronico = texto

  @property
  def departamento(self):
    return self.__departamento

  @departamento.setter
  def departamento(self, valor):
    self.__departamento = validar_texto(valor, "Departamento")

  @property
  def provincia(self):
    return self.__provincia

  @provincia.setter
  def provincia(self, valor):
    self.__provincia = validar_texto(valor, "Provincia")

  @property
  def distrito(self):
    return self.__distrito

  @distrito.setter
  def distrito(self, valor):
    self.__distrito = validar_texto(valor, "Distrito")

  @property
  def direccion(self):
    return self.__direccion

  @direccion.setter
  def direccion(self, valor):
    self.__direccion = validar_texto(valor, "Dirección")

  # ---------- Métodos ----------
  def calcular_edad(self):
    """Devuelve la edad en años cumplidos a la fecha de hoy."""
    hoy = date.today()
    nacimiento = self.__fecha_nacimiento
    cumplio_este_anio = (hoy.month, hoy.day) >= (nacimiento.month, nacimiento.day)
    return hoy.year - nacimiento.year - (0 if cumplio_este_anio else 1)
