# Modelo/__init__.py
"""Paquete Modelo (la "M" de MVC).

Permite importar todo desde un solo lugar, por ejemplo:
    from Modelo import Empresa, Requerimiento, Postulante
"""
from Modelo.excepciones import (
    DatoInvalidoError,
    DniDuplicadoError,
    ReclutamientoError,
    RegistroDuplicadoError,
    RegistroNoEncontradoError,
)
from Modelo.persona import Persona
from Modelo.tipo_afp import TipoAFP
from Modelo.profesion import Profesion
from Modelo.grado_instruccion import GradoInstruccion
from Modelo.puesto import Puesto
from Modelo.area import Area
from Modelo.regimen_laboral import RegimenLaboral
from Modelo.regimen_general import RegimenGeneral
from Modelo.regimen_agrario import RegimenAgrario
from Modelo.requerimiento import Requerimiento
from Modelo.postulante import Postulante
from Modelo.empresa import Empresa
