from tkinter import messagebox
from Modelo.excepciones import ReclutamientoError
from Modelo.requerimiento import Requerimiento
from Modelo.area import Area
from Modelo.puesto import Puesto
from Modelo.grado_instruccion import GradoInstruccion
from Modelo.profesion import Profesion
from Modelo.regimen_general import RegimenGeneral
from Modelo.regimen_agrario import RegimenAgrario
from Modelo.catalogos import REGIMENES, sueldo_puesto

class RequerimientoController:
    """Controlador para gestionar la F01 y F03 del sistema SISGER."""

    def __init__(self, xEmpresa, xVistaNuevo=None, xVistaConsultar=None):
        self.xEmpresa = xEmpresa
        self.xVistaNuevo = xVistaNuevo
        self.xVistaConsultar = xVistaConsultar

    def xRegistrarRequerimiento(self):
        try:
            xIdProceso = self.xEmpresa.siguiente_id_requerimiento()
            xFechaProceso = self.xVistaNuevo.txt_fecha_req.get()
            xNroRequeridos = int(self.xVistaNuevo.spin_nro.get())
            xNombreArea = self.xVistaNuevo.combo_area.get()
            xFechaInicio = self.xVistaNuevo.txt_fecha_ing.get()
            xFechaFinContrato = self.xVistaNuevo.txt_fecha_fin.get()
            xNombrePuesto = self.xVistaNuevo.combo_puesto.get()
            xTipoRegimen = self.xVistaNuevo.combo_regimen.get()
            xNombreGrado = self.xVistaNuevo.combo_grado.get()
            xNombreProfesion = self.xVistaNuevo.combo_profesion.get()
            xConExperiencia = bool(self.xVistaNuevo.chk_experiencia_var.get())
            xDescripcion = self.xVistaNuevo.txt_descripcion.get("1.0", "end-1c")

            xSueldoBase = sueldo_puesto(xNombreArea, xNombreGrado, xNombrePuesto)
            if xSueldoBase is None:
                raise ReclutamientoError(
                    "El puesto seleccionado no corresponde al área y grado de instrucción."
                )
            xPuesto = Puesto("P-001", xNombrePuesto, xSueldoBase)
            xArea = Area("A-001", xNombreArea, xPuesto)

            xConProfesion = xNombreGrado in ["Técnico", "Universitario"]
            xProfesion = Profesion("PR-001", xNombreProfesion) if xConProfesion else None
            xGrado = GradoInstruccion("G-001", xNombreGrado, xConProfesion, xProfesion)

            if REGIMENES.get(xTipoRegimen) == "general":
                xRegimen = RegimenGeneral("RG-001", "Régimen General 728", "Mensual", True, 9.0)
            else:
                xRegimen = RegimenAgrario("RA-001", "Régimen Agrario", "Mensual", True, 9.72, 102.50)

            xRequerimiento = Requerimiento(
                id_proceso=xIdProceso,
                fecha_proceso=xFechaProceso,
                fecha_inicio=xFechaInicio,
                fecha_fin_contrato=xFechaFinContrato,
                nro_requeridos=xNroRequeridos,
                con_experiencia=xConExperiencia,
                descripcion=xDescripcion,
                area=xArea,
                regimen_laboral=xRegimen,
                grado_instruccion=xGrado
            )

            self.xEmpresa.registrar_requerimiento(xRequerimiento)
            messagebox.showinfo(
                "Éxito", "Requerimiento registrado correctamente.",
                parent=self.xVistaNuevo.ventana,
            )
            self.xVistaNuevo.ventana.destroy()

        except ReclutamientoError as e:
            messagebox.showerror("Error de Validación", str(e), parent=self.xVistaNuevo.ventana)
        except ValueError:
            messagebox.showerror(
                "Error", "Verifique que los campos numéricos sean correctos.",
                parent=self.xVistaNuevo.ventana,
            )
        except Exception as e:
            messagebox.showerror(
                "Error", f"No se pudo registrar el requerimiento: {e}",
                parent=self.xVistaNuevo.ventana,
            )

    def xConsultarRequerimiento(self):
        xIdBusqueda = self.xVistaConsultar.txt_id.get().strip()
        if not xIdBusqueda:
            messagebox.showwarning(
                "Advertencia", "Por favor ingrese un ID de requerimiento.",
                parent=self.xVistaConsultar.ventana,
            )
            return

        try:
            xReq = self.xEmpresa.consultar_requerimiento(xIdBusqueda)
            xVista = self.xVistaConsultar

            xProfesion = xReq.grado_instruccion.profesion.nombre_profesion if xReq.grado_instruccion.profesion else "Ninguna"

            xDatos = {
                xVista.txt_fecha_req: str(xReq.fecha_proceso),
                xVista.txt_fecha_ing: str(xReq.fecha_inicio),
                xVista.txt_nro_req: str(xReq.nro_requeridos),
                xVista.txt_fecha_fin: str(xReq.fecha_fin_contrato),
                xVista.txt_area: xReq.area.nombre_area,
                xVista.txt_regimen: xReq.regimen_laboral.nombre_regimen,
                xVista.txt_puesto: xReq.area.puesto.nombre_puesto,
                xVista.txt_grado: xReq.grado_instruccion.nombre_grado,
                xVista.txt_profesion: xProfesion,
                xVista.txt_sueldo: f"S/ {xReq.area.puesto.sueldo_base:.2f}",
                xVista.txt_experiencia: "Sí" if xReq.con_experiencia else "No",
                xVista.txt_postulantes: str(xReq.obtener_nro_postulantes()),
                xVista.txt_estado: xReq.estado_requerimiento
            }
            for xCampo, xValor in xDatos.items():
                xCampo.config(state="normal")
                xCampo.delete(0, "end")
                xCampo.insert(0, xValor)
                xCampo.config(state="readonly")
            xVista.txt_descripcion.config(state="normal")
            xVista.txt_descripcion.delete("1.0", "end")
            xVista.txt_descripcion.insert("1.0", xReq.descripcion if xReq.descripcion else "Sin descripción")
            xVista.txt_descripcion.config(state="disabled")

        except ReclutamientoError as e:
            messagebox.showerror("Error", str(e), parent=self.xVistaConsultar.ventana)