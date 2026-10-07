# Modelo/excepciones.py
"""Excepciones propias del Sistema de Gestión de Reclutamiento (Unidad 4).

Todas heredan de ReclutamientoError, así el Controlador puede capturar
cualquier error del negocio con un solo `except ReclutamientoError`.
"""


class ReclutamientoError(Exception):
  """Excepción base del sistema."""


class DatoInvalidoError(ReclutamientoError):
  """Un dato no cumple las reglas de validación (vacío, formato, rango)."""


class DniDuplicadoError(ReclutamientoError):
  """Se intenta registrar un postulante con un DNI que ya existe."""


class RegistroDuplicadoError(ReclutamientoError):
  """Se intenta registrar un ID (proceso o postulante) que ya existe."""


class RegistroNoEncontradoError(ReclutamientoError):
  """Se busca un ID que no existe."""
