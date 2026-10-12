# Modelo/tipo_afp.py
from Modelo.validaciones import validar_porcentaje, validar_texto


class TipoAFP:
  """Sistema de pensiones del postulante (AFP Integra, Prima, ONP, etc.)."""

  def __init__(self, id_afp, nombre_afp, porcentaje_descuento):
    self.id_afp = id_afp
    self.nombre_afp = nombre_afp
    self.porcentaje_descuento = porcentaje_descuento

  @property
  def id_afp(self):
    return self.__id_afp

  @id_afp.setter
  def id_afp(self, valor):
    self.__id_afp = validar_texto(valor, "ID AFP")

  @property
  def nombre_afp(self):
    return self.__nombre_afp

  @nombre_afp.setter
  def nombre_afp(self, valor):
    self.__nombre_afp = validar_texto(valor, "Nombre AFP")

  @property
  def porcentaje_descuento(self):
    return self.__porcentaje_descuento

  @porcentaje_descuento.setter
  def porcentaje_descuento(self, valor):
    self.__porcentaje_descuento = validar_porcentaje(valor, "Porcentaje de Descuento")
