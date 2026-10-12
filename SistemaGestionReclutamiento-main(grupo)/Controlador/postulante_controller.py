from tkinter import messagebox
from Modelo.excepciones import ReclutamientoError
from Modelo.postulante import Postulante
from Modelo import catalogo

class PostulanteController:
    """Controlador para gestionar la F02 y F04 del sistema SISGER."""

    def __init__(self, xEmpresa, xVistaNuevo=None, xVistaConsultar=None):
        self.xEmpresa = xEmpresa
        self.xVistaNuevo = xVistaNuevo
        self.xVistaConsultar = xVistaConsultar

    def xRegistrarPostulante(self):
        try:
            xSeleccion = self.xVistaNuevo.combo_req.get()
            if not xSeleccion:
                messagebox.showwarning("Advertencia", "Primero debe registrar un requerimiento activo.")
                return
            xIdRequerimiento = xSeleccion.split(" - ")[0]
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
            xGrado = catalogo.crear_grado_instruccion(xNombreGrado, xNombreProfesion)

            xConExperiencia = bool(self.xVistaNuevo.chk_experiencia_var.get())
            xNombreAfp = self.xVistaNuevo.combo_afp.get()
            # El porcentaje de descuento sale del catálogo (AFP 10%, ONP 13%)
            xTipoAfp = catalogo.crear_tipo_afp(xNombreAfp)

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
        xIdBusqueda = self.xVistaConsultar.txt_id.get().strip()
        if not xIdBusqueda:
            messagebox.showwarning("Advertencia", "Por favor ingrese un ID de postulante.")
            return

        try:
            xPost = self.xEmpresa.consultar_postulante(xIdBusqueda)
            xVista = self.xVistaConsultar
            xDatos = {
                xVista.txt_ape_pat: xPost.apellido_paterno,
                xVista.txt_ape_mat: xPost.apellido_materno,
                xVista.txt_nombres: xPost.nombres,
                xVista.txt_fecha_post: str(xPost.fecha_registro),
                xVista.txt_celular: xPost.celular,
                xVista.txt_edad: str(xPost.calcular_edad()),
                xVista.txt_area: xPost.requerimiento.area.nombre_area,
                xVista.txt_puesto: xPost.requerimiento.area.puesto.nombre_puesto,
                xVista.txt_regimen: xPost.requerimiento.regimen_laboral.nombre_regimen,
                xVista.txt_sueldo_base: f"S/ {xPost.requerimiento.area.puesto.sueldo_base:.2f}",
                xVista.txt_descuento: f"S/ {xPost.calcular_descuento():.2f}",
                xVista.txt_sueldo_neto: f"S/ {xPost.calcular_sueldo_neto():.2f}"
            }
            for xCampo, xValor in xDatos.items():
                xCampo.config(state="normal")
                xCampo.delete(0, "end")
                xCampo.insert(0, xValor)
                xCampo.config(state="readonly")

        except ReclutamientoError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo consultar el postulante. Detalle: {str(e)}")