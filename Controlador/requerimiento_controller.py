from tkinter import messagebox
from Modelo.excepciones import ReclutamientoError
from Modelo.requerimiento import Requerimiento
from Modelo.area import Area
from Modelo.puesto import Puesto
from Modelo.grado_instruccion import GradoInstruccion
from Modelo.profesion import Profesion
from Modelo.regimen_general import RegimenGeneral
from Modelo.regimen_agrario import RegimenAgrario

class RequerimientoController:
    """Controlador para gestionar la F01 y F03 del sistema SISGER."""

    def __init__(self, xEmpresa, xVistaNuevo=None, xVistaConsultar=None):
        self.xEmpresa = xEmpresa
        self.xVistaNuevo = xVistaNuevo
        self.xVistaConsultar = xVistaConsultar

    def xRegistrarRequerimiento(self):
        try:
            xIdProceso = self.xVistaNuevo.txt_id.get()
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

            xSueldoBase = 1500.0  # Valor de negocio simulado
            xPuesto = Puesto("P-001", xNombrePuesto, xSueldoBase)
            xArea = Area("A-001", xNombreArea, xPuesto)

            xConProfesion = xNombreGrado in ["Técnico", "Universitario"]
            xProfesion = Profesion("PR-001", xNombreProfesion) if xConProfesion else None
            xGrado = GradoInstruccion("G-001", xNombreGrado, xConProfesion, xProfesion)

            if xTipoRegimen == "728":
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
            messagebox.showinfo("Éxito", "Requerimiento registrado correctamente.")
            self.xVistaNuevo.ventana.destroy()

        except ReclutamientoError as e:
            messagebox.showerror("Error de Validación", str(e))
        except ValueError:
            messagebox.showerror("Error", "Verifique que los campos numéricos sean correctos.")

    def xConsultarRequerimiento(self):
        xIdBusqueda = self.xVistaConsultar.txt_id.get()
        try:
            xReq = self.xEmpresa.consultar_requerimiento(xIdBusqueda)
            
            self.xVistaConsultar.txt_fecha_req.config(state="normal")
            self.xVistaConsultar.txt_fecha_req.delete(0, "end")
            self.xVistaConsultar.txt_fecha_req.insert(0, str(xReq.fecha_proceso))
            self.xVistaConsultar.txt_fecha_req.config(state="readonly")

            self.xVistaConsultar.txt_nro_req.config(state="normal")
            self.xVistaConsultar.txt_nro_req.delete(0, "end")
            self.xVistaConsultar.txt_nro_req.insert(0, str(xReq.nro_requeridos))
            self.xVistaConsultar.txt_nro_req.config(state="readonly")

            self.xVistaConsultar.txt_area.config(state="normal")
            self.xVistaConsultar.txt_area.delete(0, "end")
            self.xVistaConsultar.txt_area.insert(0, xReq.area.nombre_area)
            self.xVistaConsultar.txt_area.config(state="readonly")

            self.xVistaConsultar.txt_estado.config(state="normal")
            self.xVistaConsultar.txt_estado.delete(0, "end")
            self.xVistaConsultar.txt_estado.insert(0, xReq.estado_requerimiento)
            self.xVistaConsultar.txt_estado.config(state="readonly")

        except ReclutamientoError as e:
            messagebox.showerror("Error", str(e))