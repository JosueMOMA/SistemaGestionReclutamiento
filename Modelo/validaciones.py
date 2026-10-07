# Modelo/validaciones.py
"""Funciones de validación reutilizadas por los setters de las clases.

Si un dato es incorrecto, lanzan DatoInvalidoError (Unidad 4).
"""
from datetime import date, datetime

from Modelo.excepciones import DatoInvalidoError


def validar_texto(valor, campo, obligatorio=True):
  """Valida que sea texto. Si es obligatorio, no puede estar vacío."""
  if not isinstance(valor, str):
    raise DatoInvalidoError(f"El campo '{campo}' debe ser texto.")
  valor = valor.strip()
  if obligatorio and not valor:
    raise DatoInvalidoError(f"El campo '{campo}' es obligatorio.")
  return valor


def validar_booleano(valor, campo):
  if not isinstance(valor, bool):
    raise DatoInvalidoError(f"El campo '{campo}' debe ser verdadero o falso.")
  return valor


def validar_fecha(valor, campo):
  """Acepta un objeto date o un texto 'AAAA-MM-DD' (como devuelve DateEntry)."""
  if isinstance(valor, datetime):
    return valor.date()
  if isinstance(valor, date):
    return valor
  if isinstance(valor, str):
    try:
      return datetime.strptime(valor.strip(), "%Y-%m-%d").date()
    except ValueError:
      pass
  raise DatoInvalidoError(
      f"El campo '{campo}' debe ser una fecha válida (AAAA-MM-DD)."
  )


def validar_fecha_texto(valor, campo):
  """Valida un texto con formato de fecha 'AAAA-MM-DD' y lo devuelve como texto."""
  texto = validar_texto(valor, campo)
  validar_fecha(texto, campo)
  return texto


def validar_entero_positivo(valor, campo):
  if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
    raise DatoInvalidoError(f"El campo '{campo}' debe ser un entero mayor a 0.")
  return valor


def validar_numero_no_negativo(valor, campo):
  if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor < 0:
    raise DatoInvalidoError(f"El campo '{campo}' debe ser un número mayor o igual a 0.")
  return float(valor)


def validar_porcentaje(valor, campo):
  valor = validar_numero_no_negativo(valor, campo)
  if valor > 100:
    raise DatoInvalidoError(f"El campo '{campo}' debe estar entre 0 y 100.")
  return valor


def validar_digitos(valor, campo, cantidad):
  """Valida un texto formado solo por dígitos y con una cantidad exacta (DNI, RUC)."""
  texto = validar_texto(valor, campo)
  if not (texto.isdigit() and len(texto) == cantidad):
    raise DatoInvalidoError(f"El campo '{campo}' debe tener {cantidad} dígitos.")
  return texto


def validar_tipo(valor, clase, campo):
  """Valida que un objeto relacionado sea de la clase esperada (Unidad 3)."""
  if not isinstance(valor, clase):
    raise DatoInvalidoError(
        f"El campo '{campo}' debe ser un objeto de tipo {clase.__name__}."
    )
  return valor
