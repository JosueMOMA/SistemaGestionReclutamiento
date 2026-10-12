# pruebas/test_modelo.py
# Pruebas unitarias de los métodos de negocio del Modelo.
# Ejecutar desde la carpeta del proyecto:  python -m unittest -v
import unittest
from datetime import date, timedelta

from Modelo import (
    DatoInvalidoError,
    DniDuplicadoError,
    Empresa,
    Postulante,
    RegimenFactory,
    RegimenLaboral,
    RegistroDuplicadoError,
    RegistroNoEncontradoError,
    Requerimiento,
    catalogo,
)


# --- DATOS DE APOYO (Objetos reutilizados en las pruebas) ---
def crear_requerimiento(id_proceso="REQ-001", regimen="General"):
  # Creamos un requerimiento válido para Desarrollador Python (sueldo base 3000)
  hoy = date.today()
  return Requerimiento(
      id_proceso=id_proceso,
      fecha_proceso=hoy,
      fecha_inicio=hoy + timedelta(days=7),
      fecha_fin_contrato=hoy + timedelta(days=97),
      nro_requeridos=2,
      con_experiencia=True,
      descripcion="Desarrollo del sistema",
      area=catalogo.crear_area("Tecnología", "Desarrollador Python"),
      regimen_laboral=RegimenFactory.crear_regimen(regimen),
      grado_instruccion=catalogo.crear_grado_instruccion(
          "Universitario", "Ingeniería de Sistemas"
      ),
  )


def crear_postulante(requerimiento, id_postulante="POST-001", dni="12345678",
                     fecha_nacimiento="1995-05-10", afp="AFP Integra"):
  # Creamos un postulante válido asociado al requerimiento recibido
  return Postulante(
      id_postulante=id_postulante,
      fecha_registro=date.today().strftime("%Y-%m-%d"),
      dni=dni,
      apellido_paterno="Licapa",
      apellido_materno="Infanzon",
      nombres="Gianfranco",
      sexo="Masculino",
      estado_civil="Soltero(a)",
      fecha_nacimiento=fecha_nacimiento,
      celular="987654321",
      correo_electronico="gf@mail.com",
      departamento="Lima",
      provincia="Lima",
      distrito="Surco",
      direccion="Av. Ejemplo 123",
      con_experiencia=True,
      tipo_afp=catalogo.crear_tipo_afp(afp),
      grado_instruccion=catalogo.crear_grado_instruccion("Secundaria completa"),
      requerimiento=requerimiento,
  )


# --- PRUEBAS DE CÁLCULOS (Polimorfismo y reglas de negocio) ---
class TestCalculos(unittest.TestCase):

  def test_sueldo_regimen_general(self):
    # 3000 + gratificación 500 + bonificación 9% (45) = 3545
    regimen = RegimenFactory.crear_regimen("General")
    self.assertEqual(regimen.calcular_sueldo(3000), 3545.0)

  def test_sueldo_regimen_agrario(self):
    # 3000 + CTS 9.72% (291.60) + Bono BETA 30% RMV (339) = 3630.60
    regimen = RegimenFactory.crear_regimen("Agrario")
    self.assertEqual(regimen.calcular_sueldo(3000), 3630.6)

  def test_descuento_afp_y_onp(self):
    req = crear_requerimiento()
    self.assertEqual(crear_postulante(req, afp="AFP Prima").calcular_descuento(), 300.0)
    self.assertEqual(crear_postulante(req, afp="ONP").calcular_descuento(), 390.0)

  def test_sueldo_neto_polimorfismo(self):
    # El mismo método da resultados distintos según el régimen
    neto_general = crear_postulante(crear_requerimiento()).calcular_sueldo_neto()
    neto_agrario = crear_postulante(
        crear_requerimiento(regimen="Agrario")
    ).calcular_sueldo_neto()
    self.assertEqual(neto_general, 3245.0)
    self.assertEqual(neto_agrario, 3330.6)

  def test_calcular_edad(self):
    hoy = date.today()
    nacimiento = date(hoy.year - 25, 1, 1)
    postulante = crear_postulante(crear_requerimiento(), fecha_nacimiento=nacimiento)
    self.assertEqual(postulante.calcular_edad(), 25)

  def test_clase_abstracta_no_instanciable(self):
    with self.assertRaises(TypeError):
      RegimenLaboral("X", "X", "Mensual")


# --- PRUEBAS DE CONTROL (Registro, búsqueda y listado) ---
class TestEmpresa(unittest.TestCase):

  def setUp(self):
    # Reiniciamos el Singleton para que cada prueba empiece con datos limpios
    Empresa.reiniciar_instancia()
    self.empresa = Empresa("20123456789", "Asica Farms")
    self.req = crear_requerimiento()
    self.empresa.registrar_requerimiento(self.req)

  def test_singleton_misma_instancia(self):
    otra = Empresa("20999999999", "Otra")
    self.assertIs(otra, self.empresa)
    self.assertEqual(otra.nombre_empresa, "Asica Farms")

  def test_registrar_y_consultar(self):
    post = crear_postulante(self.req)
    self.empresa.registrar_postulante(post)
    self.assertIs(self.empresa.consultar_requerimiento("REQ-001"), self.req)
    self.assertIs(self.empresa.consultar_postulante("POST-001"), post)
    self.assertEqual(self.req.obtener_nro_postulantes(), 1)
    self.assertEqual(len(self.empresa.lista_postulantes), 1)

  def test_generar_ids_correlativos(self):
    self.assertEqual(self.empresa.generar_id_requerimiento(), "REQ-002")
    self.assertEqual(self.empresa.generar_id_postulante(), "POST-001")

  def test_dni_duplicado(self):
    self.empresa.registrar_postulante(crear_postulante(self.req))
    with self.assertRaises(DniDuplicadoError):
      self.empresa.registrar_postulante(crear_postulante(self.req, id_postulante="POST-002"))

  def test_requerimiento_duplicado(self):
    with self.assertRaises(RegistroDuplicadoError):
      self.empresa.registrar_requerimiento(crear_requerimiento())

  def test_consultar_id_en_minusculas(self):
    self.assertIs(self.empresa.consultar_requerimiento(" req-001 "), self.req)

  def test_consultar_inexistente(self):
    with self.assertRaises(RegistroNoEncontradoError):
      self.empresa.consultar_postulante("POST-999")

  def test_menor_de_edad(self):
    menor = crear_postulante(self.req, fecha_nacimiento="2015-01-01")
    with self.assertRaises(DatoInvalidoError):
      self.empresa.registrar_postulante(menor)


# --- PRUEBAS DE VALIDACIONES (Excepciones en los setters) ---
class TestValidaciones(unittest.TestCase):

  def setUp(self):
    self.post = crear_postulante(crear_requerimiento())

  def test_dni_invalido(self):
    with self.assertRaises(DatoInvalidoError):
      self.post.dni = "12A"

  def test_correo_invalido(self):
    with self.assertRaises(DatoInvalidoError):
      self.post.correo_electronico = "correo"

  def test_celular_invalido(self):
    with self.assertRaises(DatoInvalidoError):
      self.post.celular = "123456789"

  def test_fecha_fin_antes_de_inicio(self):
    req = crear_requerimiento()
    with self.assertRaises(DatoInvalidoError):
      req.fecha_fin_contrato = req.fecha_inicio - timedelta(days=1)

  def test_nombre_con_numeros(self):
    with self.assertRaises(DatoInvalidoError):
      self.post.nombres = "Juan123"

  def test_nombre_con_tildes_y_enie(self):
    self.post.apellido_paterno = "  Núñez   O'Brien "
    self.assertEqual(self.post.apellido_paterno, "Núñez O'Brien")

  def test_regimen_invalido(self):
    with self.assertRaises(DatoInvalidoError):
      RegimenFactory.crear_regimen("CAS")

  def test_puesto_fuera_del_area(self):
    with self.assertRaises(DatoInvalidoError):
      catalogo.crear_area("Tecnología", "Contador")

  def test_profesion_requerida(self):
    with self.assertRaises(DatoInvalidoError):
      catalogo.crear_grado_instruccion("Técnico", "")


if __name__ == "__main__":
  unittest.main()
