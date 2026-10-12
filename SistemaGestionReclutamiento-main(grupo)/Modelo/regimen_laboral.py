# Modelo/regimen_laboral.py
from abc import ABC, abstractmethod

from Modelo.excepciones import DatoInvalidoError
from Modelo.validaciones import validar_numero_no_negativo, validar_texto


class RegimenLaboral(ABC):
  """Clase ABSTRACTA (Unidad 2). No se puede instanciar directamente.

  Obliga a sus hijas (RegimenGeneral, RegimenAgrario) a implementar
  calcular_sueldo(). Cada hija lo calcula a su manera: eso es POLIMORFISMO.
  """

  def __init__(self, id_regimen, nombre_regimen, frecuencia_pago):
    self.id_regimen = id_regimen
    self.nombre_regimen = nombre_regimen
    self.frecuencia_pago = frecuencia_pago

  @property
  def id_regimen(self):
    return self.__id_regimen

  @id_regimen.setter
  def id_regimen(self, valor):
    self.__id_regimen = validar_texto(valor, "ID Régimen")

  @property
  def nombre_regimen(self):
    return self.__nombre_regimen

  @nombre_regimen.setter
  def nombre_regimen(self, valor):
    self.__nombre_regimen = validar_texto(valor, "Nombre Régimen")

  @property
  def frecuencia_pago(self):
    return self.__frecuencia_pago

  @frecuencia_pago.setter
  def frecuencia_pago(self, valor):
    self.__frecuencia_pago = validar_texto(valor, "Frecuencia de Pago")

  @staticmethod
  def _validar_sueldo_base(sueldo_base):
    """Método protegido de apoyo para las clases hijas."""
    sueldo = validar_numero_no_negativo(sueldo_base, "Sueldo Base")
    if sueldo == 0:
      raise DatoInvalidoError("El sueldo base debe ser mayor a 0.")
    return sueldo

  @abstractmethod
  def calcular_sueldo(self, sueldo_base):
    """Devuelve el sueldo bruto mensual según el régimen."""
