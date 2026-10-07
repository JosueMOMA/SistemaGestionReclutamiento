# Modelo/puesto.py
from Modelo.excepciones import DatoInvalidoError
from Modelo.validaciones import validar_numero_no_negativo, validar_texto


class Puesto:
  """Puesto de trabajo con su sueldo base mensual."""

  def __init__(self, id_puesto, nombre_puesto, sueldo_base):
    self.id_puesto = id_puesto
    self.nombre_puesto = nombre_puesto
    self.sueldo_base = sueldo_base

  @property
  def id_puesto(self):
    return self.__id_puesto

  @id_puesto.setter
  def id_puesto(self, valor):
    self.__id_puesto = validar_texto(valor, "ID Puesto")

  @property
  def nombre_puesto(self):
    return self.__nombre_puesto

  @nombre_puesto.setter
  def nombre_puesto(self, valor):
    self.__nombre_puesto = validar_texto(valor, "Nombre Puesto")

  @property
  def sueldo_base(self):
    return self.__sueldo_base

  @sueldo_base.setter
  def sueldo_base(self, valor):
    sueldo = validar_numero_no_negativo(valor, "Sueldo Base")
    if sueldo == 0:
      raise DatoInvalidoError("El sueldo base debe ser mayor a 0.")
    self.__sueldo_base = sueldo
