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
  NIVEL_GRADO = {
      "Secundaria completa": 1,
      "Técnico": 2,
      "Universitario": 3,
  }

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

  def siguiente_id_requerimiento(self):
    """Genera el siguiente ID correlativo sin reutilizar IDs existentes."""
    return self._siguiente_id("REQ", (req.id_proceso for req in self.__lista_requerimientos))

  def siguiente_id_postulante(self):
    """Genera el siguiente ID correlativo sin reutilizar IDs existentes."""
    return self._siguiente_id("POST", (post.id_postulante for post in self.__lista_postulantes))

  @staticmethod
  def _siguiente_id(prefijo, ids_existentes):
    numeros = []
    for identificador in ids_existentes:
      try:
        if identificador.startswith(f"{prefijo}-"):
          numeros.append(int(identificador.split("-", 1)[1]))
      except (AttributeError, ValueError):
        continue
    return f"{prefijo}-{max(numeros, default=0) + 1:03d}"

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
    self._validar_compatibilidad_postulante(postulante, requerimiento)

    self.__lista_postulantes.append(postulante)
    requerimiento.agregar_postulante(postulante)  # relación en ambos sentidos

  @staticmethod
  def _validar_compatibilidad_postulante(postulante, requerimiento):
    """Comprueba al final de las validaciones generales los requisitos del puesto."""
    grado_requerido = requerimiento.grado_instruccion
    grado_postulante = postulante.grado_instruccion
    nivel_requerido = Empresa.NIVEL_GRADO.get(grado_requerido.nombre_grado)
    nivel_postulante = Empresa.NIVEL_GRADO.get(grado_postulante.nombre_grado)
    if nivel_requerido is None or nivel_postulante is None:
      raise DatoInvalidoError(
          "El grado de instrucción del requerimiento o del postulante no es válido."
      )
    if nivel_postulante < nivel_requerido:
      raise DatoInvalidoError(
          "El postulante no cumple el grado de instrucción requerido: "
          f"{grado_requerido.nombre_grado}."
      )

    profesion_requerida = grado_requerido.profesion
    profesion_postulante = grado_postulante.profesion
    nombre_requerido = (
        profesion_requerida.nombre_profesion if profesion_requerida else None
    )
    nombre_postulante = (
        profesion_postulante.nombre_profesion if profesion_postulante else None
    )
    # Un nivel superior puede cubrir el requisito académico inferior con
    # cualquiera de las profesiones propias de su nivel. Por ejemplo, un
    # universitario puede postular a un requerimiento técnico aunque su
    # profesión no tenga el mismo nombre que la carrera técnica solicitada.
    profesion_no_coincide = (
        nombre_requerido is not None
        and nombre_postulante != nombre_requerido
        and nivel_postulante == nivel_requerido
    )
    if profesion_no_coincide:
      detalle = nombre_requerido or "ninguna"
      raise DatoInvalidoError(
          f"El postulante no cumple la profesión requerida: {detalle}."
      )

    if requerimiento.con_experiencia and not postulante.con_experiencia:
      raise DatoInvalidoError(
          "El postulante no cumple el requisito de experiencia laboral."
      )

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
