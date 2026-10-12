# Modelo/regimen_agrario.py
from Modelo.regimen_laboral import RegimenLaboral
from Modelo.validaciones import (
    validar_booleano,
    validar_numero_no_negativo,
    validar_porcentaje,
)


class RegimenAgrario(RegimenLaboral):
  """Régimen laboral agrario. Hereda de RegimenLaboral (Unidad 2)."""

  def __init__(
      self,
      id_regimen,
      nombre_regimen,
      frecuencia_pago,
      incluye_cts,
      porcentaje_cts,
      bono_beta,
  ):
    super().__init__(id_regimen, nombre_regimen, frecuencia_pago)
    self.incluye_cts = incluye_cts
    self.porcentaje_cts = porcentaje_cts
    self.bono_beta = bono_beta

  @property
  def incluye_cts(self):
    return self.__incluye_cts

  @incluye_cts.setter
  def incluye_cts(self, valor):
    self.__incluye_cts = validar_booleano(valor, "Incluye CTS")

  @property
  def porcentaje_cts(self):
    return self.__porcentaje_cts

  @porcentaje_cts.setter
  def porcentaje_cts(self, valor):
    self.__porcentaje_cts = validar_porcentaje(valor, "Porcentaje CTS")

  @property
  def bono_beta(self):
    return self.__bono_beta

  @bono_beta.setter
  def bono_beta(self, valor):
    self.__bono_beta = validar_numero_no_negativo(valor, "Bono BETA")

  def calcular_sueldo(self, sueldo_base):
    """Sobrescribe el método abstracto (polimorfismo).

    Sueldo mensual = base + CTS (si se incluye en el pago) + Bono BETA.
    """
    base = self._validar_sueldo_base(sueldo_base)
    sueldo = base + self.__bono_beta
    if self.__incluye_cts:
      sueldo += base * self.__porcentaje_cts / 100
    return round(sueldo, 2)
