# Modelo/postulante.py
from Modelo.grado_instruccion import GradoInstruccion
from Modelo.persona import Persona
from Modelo.requerimiento import Requerimiento
from Modelo.tipo_afp import TipoAFP
from Modelo.validaciones import (
    validar_booleano,
    validar_fecha_texto,
    validar_texto,
    validar_tipo,
)


class Postulante(Persona):
  """Postulante a un requerimiento. HEREDA de Persona (Unidad 2).

  Relaciones (Unidad 3): 1 TipoAFP, 1 GradoInstruccion, 1 Requerimiento.
  """

  def __init__(
      self,
      id_postulante,
      fecha_registro,
      dni,
      apellido_paterno,
      apellido_materno,
      nombres,
      sexo,
      estado_civil,
      fecha_nacimiento,
      celular,
      correo_electronico,
      departamento,
      provincia,
      distrito,
      direccion,
      con_experiencia,
      tipo_afp,
      grado_instruccion,
      requerimiento,
      estado_postulante="Pendiente de Entrevista",
  ):
    # super() llama al constructor de la clase padre Persona.
    super().__init__(
        dni,
        apellido_paterno,
        apellido_materno,
        nombres,
        sexo,
        estado_civil,
        fecha_nacimiento,
        celular,
        correo_electronico,
        departamento,
        provincia,
        distrito,
        direccion,
    )
    self.id_postulante = id_postulante
    self.fecha_registro = fecha_registro
    self.con_experiencia = con_experiencia
    self.estado_postulante = estado_postulante
    self.tipo_afp = tipo_afp
    self.grado_instruccion = grado_instruccion
    self.requerimiento = requerimiento

  # ---------- Properties ----------
  @property
  def id_postulante(self):
    return self.__id_postulante

  @id_postulante.setter
  def id_postulante(self, valor):
    self.__id_postulante = validar_texto(valor, "ID Postulante")

  @property
  def fecha_registro(self):
    return self.__fecha_registro

  @fecha_registro.setter
  def fecha_registro(self, valor):
    # En el diagrama es string: se guarda como texto 'AAAA-MM-DD'.
    self.__fecha_registro = validar_fecha_texto(valor, "Fecha de Registro")

  @property
  def con_experiencia(self):
    return self.__con_experiencia

  @con_experiencia.setter
  def con_experiencia(self, valor):
    self.__con_experiencia = validar_booleano(valor, "Con Experiencia")

  @property
  def estado_postulante(self):
    return self.__estado_postulante

  @estado_postulante.setter
  def estado_postulante(self, valor):
    self.__estado_postulante = validar_texto(valor, "Estado Postulante")

  @property
  def tipo_afp(self):
    return self.__tipo_afp

  @tipo_afp.setter
  def tipo_afp(self, valor):
    self.__tipo_afp = validar_tipo(valor, TipoAFP, "Tipo AFP")

  @property
  def grado_instruccion(self):
    return self.__grado_instruccion

  @grado_instruccion.setter
  def grado_instruccion(self, valor):
    self.__grado_instruccion = validar_tipo(
        valor, GradoInstruccion, "Grado de Instrucción"
    )

  @property
  def requerimiento(self):
    return self.__requerimiento

  @requerimiento.setter
  def requerimiento(self, valor):
    self.__requerimiento = validar_tipo(valor, Requerimiento, "Requerimiento")

  # ---------- Métodos ----------
  def calcular_descuento(self):
    """Aporte al sistema de pensiones: % de la AFP/ONP sobre el sueldo base.

    (Gratificación, CTS y Bono BETA no están afectos al aporte previsional.)
    """
    sueldo_base = self.__requerimiento.area.puesto.sueldo_base
    return round(sueldo_base * self.__tipo_afp.porcentaje_descuento / 100, 2)

  def calcular_sueldo_neto(self):
    """Sueldo neto = sueldo del régimen - descuento de pensiones.

    POLIMORFISMO: no importa si el régimen es General o Agrario,
    se llama al mismo método calcular_sueldo() y cada clase responde a su manera.
    """
    sueldo_base = self.__requerimiento.area.puesto.sueldo_base
    sueldo_bruto = self.__requerimiento.regimen_laboral.calcular_sueldo(sueldo_base)
    return round(sueldo_bruto - self.calcular_descuento(), 2)
