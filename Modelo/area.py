# Modelo/area.py
from Modelo.puesto import Puesto
from Modelo.validaciones import validar_texto, validar_tipo


class Area:
  """Área de la empresa. Relación (Unidad 3): Area -> 1 Puesto (según el diagrama)."""

  def __init__(self, id_area, nombre_area, puesto):
    self.id_area = id_area
    self.nombre_area = nombre_area
    self.puesto = puesto

  @property
  def id_area(self):
    return self.__id_area

  @id_area.setter
  def id_area(self, valor):
    self.__id_area = validar_texto(valor, "ID Área")

  @property
  def nombre_area(self):
    return self.__nombre_area

  @nombre_area.setter
  def nombre_area(self, valor):
    self.__nombre_area = validar_texto(valor, "Nombre Área")

  @property
  def puesto(self):
    return self.__puesto

  @puesto.setter
  def puesto(self, valor):
    self.__puesto = validar_tipo(valor, Puesto, "Puesto")
