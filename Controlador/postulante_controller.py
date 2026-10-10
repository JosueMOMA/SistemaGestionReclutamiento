from tkinter import messagebox
from Modelo.excepciones import ReclutamientoError
from Modelo.postulante import Postulante
from Modelo.tipo_afp import TipoAFP
from Modelo.grado_instruccion import GradoInstruccion
from Modelo.profesion import Profesion

class PostulanteController:
    """Controlador para gestionar la F02 y F04 del sistema SISGER."""

    def __init__(self, xEmpresa, xVistaNuevo=None, xVistaConsultar=None):
        self.xEmpresa = xEmpresa
        self.xVistaNuevo = xVistaNuevo
        self.xVistaConsultar = xVistaConsultar

    def xRegistrarPostulante(self):
        try:
            xIdRequerimiento = self.xVistaNuevo.combo_req.get().split(" - ")[0]
            xRequerimiento = self.xEmpresa.consultar_requerimiento(xIdRequerimiento)

            xIdPostulante = self.xVistaNuevo.txt_id.get()
            xFechaRegistro = self.xVistaNuevo.txt_fecha_post.get()
            xDni = self.xVistaNuevo.txt_dni.get()
            xApePaterno = self.xVistaNuevo.txt_ape_pat.get()
            xApeMaterno = self.xVistaNuevo.txt_ape_mat.get()
            xNombres = self.xVistaNuevo.txt_nombres.get()
            xSexo = self.xVistaNuevo.combo_sexo.get()
            xEstadoCivil = self.xVistaNuevo.combo_estado_civil.get()
            xFechaNac = self.xVistaNuevo.date_nacimiento.get()
            xCelular = self.xVistaNuevo.txt_celular.get()
            xCorreo = self.xVistaNuevo.txt_correo.get()
            xDepartamento = self.xVistaNuevo.combo_dep.get()
            xProvincia = self.xVistaNuevo.combo_prov.get()
            xDistrito = self.xVistaNuevo.combo_dist.get()
            xDireccion = self.xVistaNuevo.txt_direccion.get()
            
            xNombreGrado = self.xVistaNuevo.combo_grado.get()
            xNombreProfesion = self.xVistaNuevo.combo_profesion.get()
            xConProfesion = xNombreGrado in ["Técnico", "Universitario"]
            xProfesion = Profesion("PR-001", xNombreProfesion) if xConProfesion else None
            xGrado = GradoInstruccion("G-002", xNombreGrado, xConProfesion, xProfesion)

            xConExperiencia = bool(self.xVistaNuevo.chk_experiencia_var.get())
            xNombreAfp = self.xVistaNuevo.combo_afp.get()
            xTipoAfp = TipoAFP("AFP-1", xNombreAfp, 12.0)

            xPostulante = Postulante(
                id_postulante=xIdPostulante,
                fecha_registro=xFechaRegistro,
                dni=xDni,
                apellido_paterno=xApePaterno,
                apellido_materno=xApeMaterno,
                nombres=xNombres,
                sexo=xSexo,
                estado_civil=xEstadoCivil,
                fecha_nacimiento=xFechaNac,
                celular=xCelular,
                correo_electronico=xCorreo,
                departamento=xDepartamento,
                provincia=xProvincia,
                distrito=xDistrito,
                direccion=xDireccion,
                con_experiencia=xConExperiencia,
                tipo_afp=xTipoAfp,
                grado_instruccion=xGrado,
                requerimiento=xRequerimiento
            )

            self.xEmpresa.registrar_postulante(xPostulante)
            messagebox.showinfo("Éxito", "Postulante registrado correctamente.")
            self.xVistaNuevo.ventana.destroy()

        except ReclutamientoError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Verifique los datos ingresados. Detalle: {str(e)}")

    def xConsultarPostulante(self):
        xIdBusqueda = self.xVistaConsultar.txt_id.get()
        try:
            xPost = self.xEmpresa.consultar_postulante(xIdBusqueda)
            
            self.xVistaConsultar.txt_ape_pat.config(state="normal")
            self.xVistaConsultar.txt_ape_pat.delete(0, "end")
            self.xVistaConsultar.txt_ape_pat.insert(0, xPost.apellido_paterno)
            self.xVistaConsultar.txt_ape_pat.config(state="readonly")

            self.xVistaConsultar.txt_nombres.config(state="normal")
            self.xVistaConsultar.txt_nombres.delete(0, "end")
            self.xVistaConsultar.txt_nombres.insert(0, xPost.nombres)
            self.xVistaConsultar.txt_nombres.config(state="readonly")

            xSueldoNeto = xPost.calcular_sueldo_neto()
            self.xVistaConsultar.txt_sueldo_neto.config(state="normal")
            self.xVistaConsultar.txt_sueldo_neto.delete(0, "end")
            self.xVistaConsultar.txt_sueldo_neto.insert(0, f"S/ {xSueldoNeto:.2f}")
            self.xVistaConsultar.txt_sueldo_neto.config(state="readonly")

        except ReclutamientoError as e:
            messagebox.showerror("Error", str(e))