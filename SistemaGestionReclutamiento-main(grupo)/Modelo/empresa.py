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

  PATRÓN DE DISEÑO SINGLETON: solo existe UNA instancia de Empresa en todo
  el sistema. Así todas las ventanas y controladores comparten las mismas
  listas de requerimientos y postulantes.
  """

  EDAD_MINIMA = 18
  _instancia = None  # aquí se guarda la única instancia (Singleton)

  def __new__(cls, *args, **kwargs):
    # Si ya existe una Empresa, devolvemos la misma en lugar de crear otra
    if cls._instancia is None:
      cls._instancia = super().__new__(cls)
    return cls._instancia

  def __init__(self, ruc_empresa, nombre_empresa):
    # Evitamos reiniciar las listas si la instancia ya fue creada antes
    if getattr(self, "_Empresa__inicializada", False):
      return
    self.ruc_empresa = ruc_empresa
    self.nombre_empresa = nombre_empresa
    self.__lista_requerimientos = []
    self.__lista_postulantes = []
    self.__inicializada = True

  @classmethod
  def obtener_instancia(cls):
    # Devolvemos la instancia única (None si aún no se creó)
    return cls._instancia

  @classmethod
  def reiniciar_instancia(cls):
    # Borramos la instancia única (se usa en las pruebas unitarias)
    cls._instancia = None

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
    id_proceso = self.__normalizar_id(id_proceso, "ID Proceso")
    for req in self.__lista_requerimientos:
      if req.id_proceso == id_proceso:
        return req
    raise RegistroNoEncontradoError(f"No existe el proceso {id_proceso}.")

  def consultar_postulante(self, id_postulante):
    id_postulante = self.__normalizar_id(id_postulante, "ID Postulante")
    for post in self.__lista_postulantes:
      if post.id_postulante == id_postulante:
        return post
    raise RegistroNoEncontradoError(f"No existe el postulante {id_postulante}.")

  def generar_id_requerimiento(self):
    # Generamos el siguiente ID correlativo, ej. REQ-001, REQ-002...
    return self.__generar_id("REQ", [r.id_proceso for r in self.__lista_requerimientos])

  def generar_id_postulante(self):
    # Generamos el siguiente ID correlativo, ej. POST-001, POST-002...
    return self.__generar_id("POST", [p.id_postulante for p in self.__lista_postulantes])

  @staticmethod
  def __normalizar_id(valor, campo):
    # Aceptamos el ID en minúsculas o con espacios (ej. " req-001 " -> "REQ-001")
    texto = validar_texto(valor, campo).upper()
    if len(texto) > 20:
      raise DatoInvalidoError(f"El {campo} ingresado no es válido.")
    return texto

  @staticmethod
  def __generar_id(prefijo, ids_existentes):
    # Tomamos el mayor número usado y le sumamos 1
    numeros = [
        int(i.split("-")[1]) for i in ids_existentes
        if i.startswith(prefijo + "-") and i.split("-")[1].isdigit()
    ]
    return f"{prefijo}-{(max(numeros) if numeros else 0) + 1:03d}"
