# Modelo/regimen_factory.py
# PATRÓN DE DISEÑO FACTORY (Fábrica)
# Centralizamos la creación de los regímenes laborales: quien lo usa solo indica
# el tipo ("General" o "Agrario") y la fábrica devuelve el objeto correcto.
# Si mañana se agrega un nuevo régimen, solo se modifica esta clase.
from Modelo import catalogo
from Modelo.excepciones import DatoInvalidoError
from Modelo.regimen_agrario import RegimenAgrario
from Modelo.regimen_general import RegimenGeneral


class RegimenFactory:

  TIPOS = ("General", "Agrario")

  @staticmethod
  def obtener_tipos():
    # Devolvemos los tipos disponibles para llenar el combo de la Vista
    return list(RegimenFactory.TIPOS)

  @staticmethod
  def crear_regimen(tipo):
    # Creamos el objeto hijo de RegimenLaboral según el tipo solicitado
    if tipo == "General":
      return RegimenGeneral(
          "RG-01",
          "General",
          "Mensual",
          incluye_gratificacion=True,
          porcentaje_essalud=catalogo.PORCENTAJE_ESSALUD,
      )
    if tipo == "Agrario":
      bono_beta = round(
          catalogo.RMV_REFERENCIAL * catalogo.PORCENTAJE_BONO_BETA / 100, 2
      )
      return RegimenAgrario(
          "RG-02",
          "Agrario",
          "Mensual",
          incluye_cts=True,
          porcentaje_cts=catalogo.PORCENTAJE_CTS_AGRARIO,
          bono_beta=bono_beta,
      )
    raise DatoInvalidoError(
        f"El régimen '{tipo}' no es válido. Opciones: {', '.join(RegimenFactory.TIPOS)}."
    )
