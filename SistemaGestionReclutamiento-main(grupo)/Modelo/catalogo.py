# Modelo/catalogo.py
# Datos maestros del sistema (áreas, puestos, sueldos, AFP, grados y profesiones).
# Centralizamos aquí los valores para que la Vista y el Controlador no los escriban a mano.
from Modelo.area import Area
from Modelo.grado_instruccion import GradoInstruccion
from Modelo.profesion import Profesion
from Modelo.puesto import Puesto
from Modelo.tipo_afp import TipoAFP
from Modelo.excepciones import DatoInvalidoError

# --- PARÁMETROS LEGALES (Valores referenciales, actualizar si cambian) ---
RMV_REFERENCIAL = 1130.0           # Remuneración Mínima Vital usada como referencia
PORCENTAJE_BONO_BETA = 30.0        # Bono BETA del régimen agrario = 30% de la RMV
PORCENTAJE_ESSALUD = 9.0           # Bonificación extraordinaria sobre la gratificación
PORCENTAJE_CTS_AGRARIO = 9.72      # CTS incluida en la remuneración agraria

# --- ÁREAS Y PUESTOS (Sueldo base mensual referencial en soles) ---
AREAS_PUESTOS = {
    "Tecnología": {
        "Desarrollador Python": 3000.0,
        "Analista de Sistemas": 2800.0,
    },
    "Recursos Humanos": {
        "Analista de RRHH": 2500.0,
        "Asistente de RRHH": 1600.0,
    },
    "Administración": {
        "Asistente Administrativo": 1500.0,
        "Contador": 2800.0,
    },
    "Operaciones": {
        "Operario de Campo": 1200.0,
        "Supervisor de Campo": 2200.0,
    },
}

# --- SISTEMA DE PENSIONES (Aporte obligatorio en %) ---
TIPOS_AFP = {
    "AFP Integra": 10.0,
    "AFP Habitat": 10.0,
    "AFP Prima": 10.0,
    "AFP Profuturo": 10.0,
    "ONP": 13.0,
}

# --- EDUCACIÓN ---
GRADOS_INSTRUCCION = {
    # nombre del grado: ¿requiere profesión?
    "Secundaria completa": False,
    "Técnico": True,
    "Universitario": True,
}

PROFESIONES = [
    "Ingeniería de Sistemas",
    "Administración",
    "Contabilidad",
    "Psicología",
]


# --- FUNCIONES DE CONSULTA (Para llenar los combos de la Vista) ---
def obtener_areas():
  return list(AREAS_PUESTOS.keys())


def obtener_puestos(nombre_area):
  # Devolvemos los puestos que pertenecen al área seleccionada
  return list(AREAS_PUESTOS.get(nombre_area, {}).keys())


def obtener_tipos_afp():
  return list(TIPOS_AFP.keys())


def obtener_grados():
  return list(GRADOS_INSTRUCCION.keys())


def obtener_profesiones():
  return list(PROFESIONES)


# --- FUNCIONES DE CREACIÓN (Construyen los objetos del Modelo) ---
def _codigo(prefijo, lista, nombre):
  # Generamos un código estable a partir de la posición del elemento, ej. "AR-01"
  return f"{prefijo}-{lista.index(nombre) + 1:02d}"


def crear_area(nombre_area, nombre_puesto):
  # Creamos el Área con su Puesto y el sueldo base del catálogo
  if nombre_area not in AREAS_PUESTOS:
    raise DatoInvalidoError(f"El área '{nombre_area}' no existe en el catálogo.")
  puestos = AREAS_PUESTOS[nombre_area]
  if nombre_puesto not in puestos:
    raise DatoInvalidoError(
        f"El puesto '{nombre_puesto}' no pertenece al área '{nombre_area}'."
    )
  puesto = Puesto(
      _codigo("PU", list(puestos), nombre_puesto), nombre_puesto, puestos[nombre_puesto]
  )
  return Area(_codigo("AR", obtener_areas(), nombre_area), nombre_area, puesto)


def crear_tipo_afp(nombre_afp):
  # Creamos el TipoAFP con su porcentaje de descuento según el catálogo
  if nombre_afp not in TIPOS_AFP:
    raise DatoInvalidoError(f"El sistema de pensiones '{nombre_afp}' no existe.")
  return TipoAFP(
      _codigo("AFP", obtener_tipos_afp(), nombre_afp), nombre_afp, TIPOS_AFP[nombre_afp]
  )


def crear_grado_instruccion(nombre_grado, nombre_profesion=""):
  # Creamos el grado y, si lo requiere, su profesión
  if nombre_grado not in GRADOS_INSTRUCCION:
    raise DatoInvalidoError(f"El grado de instrucción '{nombre_grado}' no existe.")
  con_profesion = GRADOS_INSTRUCCION[nombre_grado]
  profesion = None
  if con_profesion:
    if nombre_profesion not in PROFESIONES:
      raise DatoInvalidoError(
          f"Seleccione una profesión para el grado '{nombre_grado}'."
      )
    profesion = Profesion(
        _codigo("PR", PROFESIONES, nombre_profesion), nombre_profesion
    )
  return GradoInstruccion(
      _codigo("GI", obtener_grados(), nombre_grado), nombre_grado, con_profesion, profesion
  )
