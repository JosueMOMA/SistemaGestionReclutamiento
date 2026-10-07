# Modelo/regimen_general.py
from Modelo.regimen_laboral import RegimenLaboral
from Modelo.validaciones import validar_booleano, validar_porcentaje


class RegimenGeneral(RegimenLaboral):
  """Régimen laboral general. Hereda de RegimenLaboral (Unidad 2)."""

  def __init__(
      self,
      id_regimen,
      nombre_regimen,
      frecuencia_pago,
      incluye_gratificacion,
      porcentaje_essalud,
  ):
    super().__init__(id_regimen, nombre_regimen, frecuencia_pago)
    self.incluye_gratificacion = incluye_gratificacion
    self.porcentaje_essalud = porcentaje_essalud

  @property
  def incluye_gratificacion(self):
    return self.__incluye_gratificacion

  @incluye_gratificacion.setter
  def incluye_gratificacion(self, valor):
    self.__incluye_gratificacion = validar_booleano(valor, "Incluye Gratificación")

  @property
  def porcentaje_essalud(self):
    return self.__porcentaje_essalud

  @porcentaje_essalud.setter
  def porcentaje_essalud(self, valor):
    self.__porcentaje_essalud = validar_porcentaje(valor, "Porcentaje EsSalud")

  def calcular_sueldo(self, sueldo_base):
    """Sobrescribe el método abstracto (polimorfismo).

    Sueldo mensual = base + gratificación prorrateada + bonificación extraordinaria.
    - Gratificación: 2 sueldos al año (julio y diciembre) -> base * 2 / 12 al mes.
    - Bonificación extraordinaria: % de EsSalud sobre la gratificación.
    """
    base = self._validar_sueldo_base(sueldo_base)
    sueldo = base
    if self.__incluye_gratificacion:
      gratificacion_mensual = base * 2 / 12
      bonificacion = gratificacion_mensual * self.__porcentaje_essalud / 100
      sueldo += gratificacion_mensual + bonificacion
    return round(sueldo, 2)
