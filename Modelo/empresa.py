# Modelo/empresa.py
from Modelo.excepciones import (
    DatoInvalidoError,
    DniDuplicadoError,
    RegistroDuplicadoError,
    RegistroNoEncontradoError,
)
from Modelo.postulante import Postulante
from Modelo.requerimiento import Requerimiento
from Modelo.validaciones import validar_digitos, validar_texto, validar_tipo


class Empresa:
  """Empresa que administra los requerimientos y postulantes.

  Unidad 1: guarda LISTAS de objetos.
  Unidad 3: Empresa tiene 0..* Requerimiento y 0..* Postulante.
  Unidad 4: lanza excepciones propias ante duplicados o búsquedas fallidas.
  """

  EDAD_MINIMA = 18

  def __init__(self, ruc_empresa, nombre_empresa):
    self.ruc_empresa = ruc_empresa
    self.nombre_empresa = nombre_empresa
    self.__lista_requerimientos = []
    self.__lista_postulantes = []

  # ---------- Properties ----------
  @property
  def ruc_empresa(self):
    return self.__ruc_empresa

  @ruc_empresa.setter
  def ruc_empresa(self, valor):
    self.__ruc_empresa = validar_digitos(valor, "RUC", 11)

  @property
  def nombre_empresa(self):
    return self.__nombre_empresa

  @nombre_empresa.setter
  def nombre_empresa(self, valor):
    self.__nombre_empresa = validar_texto(valor, "Nombre Empresa")

  @property
  def lista_requerimientos(self):
    """Solo lectura: para agregar se usa registrar_requerimiento()."""
    return list(self.__lista_requerimientos)

  @property
  def lista_postulantes(self):
    """Solo lectura: para agregar se usa registrar_postulante()."""
    return list(self.__lista_postulantes)

  # ---------- Métodos ----------
  def registrar_requerimiento(self, requerimiento):
    validar_tipo(requerimiento, Requerimiento, "Requerimiento")
    for req in self.__lista_requerimientos:
      if req.id_proceso == requerimiento.id_proceso:
        raise RegistroDuplicadoError(
            f"Ya existe un requerimiento con ID Proceso {requerimiento.id_proceso}."
        )
    self.__lista_requerimientos.append(requerimiento)

  def registrar_postulante(self, postulante):
    validar_tipo(postulante, Postulante, "Postulante")
    for post in self.__lista_postulantes:
      if post.id_postulante == postulante.id_postulante:
        raise RegistroDuplicadoError(
            f"Ya existe un postulante con ID {postulante.id_postulante}."
        )
      if post.dni == postulante.dni:
        raise DniDuplicadoError(
            f"El DNI {postulante.dni} ya está registrado."
        )

    requerimiento = postulante.requerimiento
    if requerimiento not in self.__lista_requerimientos:
      raise RegistroNoEncontradoError(
          f"El requerimiento {requerimiento.id_proceso} no está registrado en la empresa."
      )
    if requerimiento.estado_requerimiento != "Activo":
      raise DatoInvalidoError(
          f"El requerimiento {requerimiento.id_proceso} no está activo."
      )
    if postulante.calcular_edad() < self.EDAD_MINIMA:
      raise DatoInvalidoError(
          f"El postulante debe tener al menos {self.EDAD_MINIMA} años."
      )

    self.__lista_postulantes.append(postulante)
    requerimiento.agregar_postulante(postulante)  # relación en ambos sentidos

  def consultar_requerimiento(self, id_proceso):
    id_proceso = validar_texto(id_proceso, "ID Proceso")
    for req in self.__lista_requerimientos:
      if req.id_proceso == id_proceso:
        return req
    raise RegistroNoEncontradoError(f"No existe el proceso {id_proceso}.")

  def consultar_postulante(self, id_postulante):
    id_postulante = validar_texto(id_postulante, "ID Postulante")
    for post in self.__lista_postulantes:
      if post.id_postulante == id_postulante:
        return post
    raise RegistroNoEncontradoError(f"No existe el postulante {id_postulante}.")
