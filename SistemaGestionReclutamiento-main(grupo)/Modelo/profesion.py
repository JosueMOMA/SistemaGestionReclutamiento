# Modelo/profesion.py
from Modelo.validaciones import validar_texto


class Profesion:
  """Profesión asociada a un grado de instrucción (Técnico o Universitario)."""

  def __init__(self, id_profesion, nombre_profesion):
    self.id_profesion = id_profesion
    self.nombre_profesion = nombre_profesion

  @property
  def id_profesion(self):
    return self.__id_profesion

  @id_profesion.setter
  def id_profesion(self, valor):
    self.__id_profesion = validar_texto(valor, "ID Profesión")

  @property
  def nombre_profesion(self):
    return self.__nombre_profesion

  @nombre_profesion.setter
  def nombre_profesion(self, valor):
    self.__nombre_profesion = validar_texto(valor, "Nombre Profesión")
