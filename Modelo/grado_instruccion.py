# Modelo/grado_instruccion.py
from Modelo.excepciones import DatoInvalidoError
from Modelo.profesion import Profesion
from Modelo.validaciones import validar_booleano, validar_texto, validar_tipo


class GradoInstruccion:
  """Grado de instrucción. Si con_profesion es True, debe tener una Profesion.

  Relación (Unidad 3): GradoInstruccion -> 1 Profesion.
  """

  def __init__(self, id_grado_instruccion, nombre_grado, con_profesion, profesion=None):
    self.id_grado_instruccion = id_grado_instruccion
    self.nombre_grado = nombre_grado
    self.__con_profesion = validar_booleano(con_profesion, "Con Profesión")
    self.profesion = profesion

  @property
  def id_grado_instruccion(self):
    return self.__id_grado_instruccion

  @id_grado_instruccion.setter
  def id_grado_instruccion(self, valor):
    self.__id_grado_instruccion = validar_texto(valor, "ID Grado de Instrucción")

  @property
  def nombre_grado(self):
    return self.__nombre_grado

  @nombre_grado.setter
  def nombre_grado(self, valor):
    self.__nombre_grado = validar_texto(valor, "Nombre del Grado")

  @property
  def con_profesion(self):
    return self.__con_profesion

  @con_profesion.setter
  def con_profesion(self, valor):
    self.__con_profesion = validar_booleano(valor, "Con Profesión")
    if not valor:
      self.__profesion = None  # sin profesión, se limpia la relación

  @property
  def profesion(self):
    return self.__profesion

  @profesion.setter
  def profesion(self, valor):
    if valor is None:
      if self.__con_profesion:
        raise DatoInvalidoError(
            f"El grado '{self.__nombre_grado}' requiere una profesión."
        )
    else:
      if not self.__con_profesion:
        raise DatoInvalidoError(
            f"El grado '{self.__nombre_grado}' no admite profesión."
        )
      validar_tipo(valor, Profesion, "Profesión")
    self.__profesion = valor
