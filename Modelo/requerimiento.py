# Modelo/requerimiento.py
from Modelo.area import Area
from Modelo.excepciones import DatoInvalidoError, RegistroDuplicadoError
from Modelo.grado_instruccion import GradoInstruccion
from Modelo.regimen_laboral import RegimenLaboral
from Modelo.validaciones import (
    validar_booleano,
    validar_entero_positivo,
    validar_fecha,
    validar_texto,
    validar_tipo,
)


class Requerimiento:
  """Requerimiento de personal (proceso de reclutamiento).

  Relaciones (Unidad 3):
    - 1 Area, 1 RegimenLaboral, 1 GradoInstruccion
    - 0..* Postulante (lista de objetos, Unidad 1)
  """

  def __init__(
      self,
      id_proceso,
      fecha_proceso,
      fecha_inicio,
      fecha_fin_contrato,
      nro_requeridos,
      con_experiencia,
      descripcion,
      area,
      regimen_laboral,
      grado_instruccion,
      estado_requerimiento="Activo",
  ):
    # Se inicializan en None porque los setters de fechas se validan entre sí.
    self.__fecha_proceso = None
    self.__fecha_inicio = None
    self.__fecha_fin_contrato = None
    self.__postulantes = []  # lista de objetos Postulante

    self.id_proceso = id_proceso
    self.fecha_proceso = fecha_proceso
    self.fecha_inicio = fecha_inicio
    self.fecha_fin_contrato = fecha_fin_contrato
    self.nro_requeridos = nro_requeridos
    self.con_experiencia = con_experiencia
    self.descripcion = descripcion
    self.area = area
    self.regimen_laboral = regimen_laboral
    self.grado_instruccion = grado_instruccion
    self.estado_requerimiento = estado_requerimiento

  # ---------- Properties ----------
  @property
  def id_proceso(self):
    return self.__id_proceso

  @id_proceso.setter
  def id_proceso(self, valor):
    self.__id_proceso = validar_texto(valor, "ID Proceso")

  @property
  def fecha_proceso(self):
    return self.__fecha_proceso

  @fecha_proceso.setter
  def fecha_proceso(self, valor):
    fecha = validar_fecha(valor, "Fecha Proceso")
    if self.__fecha_inicio and self.__fecha_inicio < fecha:
      raise DatoInvalidoError(
          "La fecha de proceso no puede ser posterior a la fecha de inicio."
      )
    self.__fecha_proceso = fecha

  @property
  def fecha_inicio(self):
    return self.__fecha_inicio

  @fecha_inicio.setter
  def fecha_inicio(self, valor):
    fecha = validar_fecha(valor, "Fecha Inicio")
    if self.__fecha_proceso and fecha < self.__fecha_proceso:
      raise DatoInvalidoError(
          "La fecha de inicio no puede ser anterior a la fecha de proceso."
      )
    if self.__fecha_fin_contrato and self.__fecha_fin_contrato <= fecha:
      raise DatoInvalidoError(
          "La fecha de inicio debe ser anterior a la fecha de fin de contrato."
      )
    self.__fecha_inicio = fecha

  @property
  def fecha_fin_contrato(self):
    return self.__fecha_fin_contrato

  @fecha_fin_contrato.setter
  def fecha_fin_contrato(self, valor):
    fecha = validar_fecha(valor, "Fecha Fin Contrato")
    if self.__fecha_inicio and fecha <= self.__fecha_inicio:
      raise DatoInvalidoError(
          "La fecha de fin de contrato debe ser posterior a la fecha de inicio."
      )
    self.__fecha_fin_contrato = fecha

  @property
  def nro_requeridos(self):
    return self.__nro_requeridos

  @nro_requeridos.setter
  def nro_requeridos(self, valor):
    self.__nro_requeridos = validar_entero_positivo(valor, "Nro Requeridos")

  @property
  def con_experiencia(self):
    return self.__con_experiencia

  @con_experiencia.setter
  def con_experiencia(self, valor):
    self.__con_experiencia = validar_booleano(valor, "Con Experiencia")

  @property
  def descripcion(self):
    return self.__descripcion

  @descripcion.setter
  def descripcion(self, valor):
    self.__descripcion = validar_texto(valor, "Descripción", obligatorio=False)

  @property
  def estado_requerimiento(self):
    return self.__estado_requerimiento

  @estado_requerimiento.setter
  def estado_requerimiento(self, valor):
    self.__estado_requerimiento = validar_texto(valor, "Estado Requerimiento")

  @property
  def area(self):
    return self.__area

  @area.setter
  def area(self, valor):
    self.__area = validar_tipo(valor, Area, "Área")

  @property
  def regimen_laboral(self):
    return self.__regimen_laboral

  @regimen_laboral.setter
  def regimen_laboral(self, valor):
    # Acepta cualquier hija de RegimenLaboral (General o Agrario).
    self.__regimen_laboral = validar_tipo(valor, RegimenLaboral, "Régimen Laboral")

  @property
  def grado_instruccion(self):
    return self.__grado_instruccion

  @grado_instruccion.setter
  def grado_instruccion(self, valor):
    self.__grado_instruccion = validar_tipo(
        valor, GradoInstruccion, "Grado de Instrucción"
    )

  @property
  def postulantes(self):
    """Solo lectura: devuelve una copia para proteger la lista interna."""
    return list(self.__postulantes)

  # ---------- Métodos ----------
  def agregar_postulante(self, postulante):
    """Asocia un postulante a este requerimiento (lo usa Empresa)."""
    # Import local para evitar importación circular con postulante.py
    from Modelo.postulante import Postulante

    validar_tipo(postulante, Postulante, "Postulante")
    if postulante in self.__postulantes:
      raise RegistroDuplicadoError(
          f"El postulante {postulante.id_postulante} ya está en el proceso "
          f"{self.__id_proceso}."
      )
    self.__postulantes.append(postulante)

  def obtener_nro_postulantes(self):
    return len(self.__postulantes)
