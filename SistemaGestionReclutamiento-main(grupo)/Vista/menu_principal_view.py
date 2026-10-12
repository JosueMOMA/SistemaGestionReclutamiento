import tkinter as tk
from tkinter import messagebox
from Vista.nuevo_requerimiento_view import NuevoRequerimientoView
from Vista.consultar_requerimiento_view import ConsultarRequerimientoView
from Vista.nuevo_postulante_view import NuevoPostulanteView
from Vista.consultar_postulante_view import ConsultarPostulanteView
from Vista.listar_requerimientos_view import ListarRequerimientosView  
from Vista.listar_postulantes_view import ListarPostulantesView  
from Vista.informacion_sistema_view import InformacionSistemaView  

class MenuPrincipalView:

    def __init__(self, root, xEmpresa):
        self.ventana = root
        self.xEmpresa = xEmpresa
        self.ventana.title("Sistema de Gestión de Reclutamiento")

        ancho_ventana = 580
        alto_ventana = 300
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        self.crear_menu()
        self.crear_bienvenida()

    def crear_bienvenida(self):
        # Mensaje de bienvenida en la ventana principal
        xFrame = tk.Frame(self.ventana)
        xFrame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(xFrame, text="SISGER", font=("Arial", 22, "bold")).pack()
        tk.Label(xFrame, text="Sistema de Gestión de Reclutamiento", font=("Arial", 12)).pack(pady=(0, 4))
        tk.Label(xFrame, text=self.xEmpresa.nombre_empresa, font=("Arial", 10, "italic")).pack()
        tk.Label(
            xFrame, text="Seleccione una opción del menú superior para comenzar.",
            font=("Arial", 9), fg="gray30"
        ).pack(pady=(18, 0))

    def abrir_nuevo_requerimiento(self):
        NuevoRequerimientoView(self.ventana, self.xEmpresa)
        
    def abrir_consultar_requerimiento(self):
        ConsultarRequerimientoView(self.ventana, self.xEmpresa)
        
    def abrir_nuevo_postulante(self):
        NuevoPostulanteView(self.ventana, self.xEmpresa)
        
    def abrir_consultar_postulante(self):
        ConsultarPostulanteView(self.ventana, self.xEmpresa)
        
    def abrir_listar_requerimientos(self):
        try:
            self._listar_requerimientos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el listado. Detalle: {e}")

    def abrir_listar_postulantes(self):
        try:
            self._listar_postulantes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el listado. Detalle: {e}")

    def _listar_requerimientos(self):
        registros = [
            (req.id_proceso, req.fecha_proceso, req.fecha_inicio, req.fecha_fin_contrato,
             req.nro_requeridos, req.obtener_nro_postulantes(), req.estado_requerimiento)
            for req in self.xEmpresa.lista_requerimientos
        ]
        ListarRequerimientosView(self.ventana, registros)
        
    def _listar_postulantes(self):
        registros = [
            (post.id_postulante, post.fecha_registro, post.dni, post.requerimiento.area.nombre_area,
             post.requerimiento.area.puesto.nombre_puesto, post.estado_postulante)
            for post in self.xEmpresa.lista_postulantes
        ]
        ListarPostulantesView(self.ventana, registros)
        
    def abrir_informacion_sistema(self):  
        InformacionSistemaView(self.ventana)

    def crear_menu(self):
        barra_menu = tk.Menu(self.ventana)

        menu_requerimiento = tk.Menu(barra_menu, tearoff=0)
        menu_requerimiento.add_command(label="Nuevo requerimiento", command=self.abrir_nuevo_requerimiento)
        menu_requerimiento.add_command(label="Consultar requerimiento", command=self.abrir_consultar_requerimiento)
        barra_menu.add_cascade(label="Requerimiento", menu=menu_requerimiento)

        menu_postulante = tk.Menu(barra_menu, tearoff=0)
        menu_postulante.add_command(label="Nuevo postulante", command=self.abrir_nuevo_postulante)
        menu_postulante.add_command(label="Consultar postulante", command=self.abrir_consultar_postulante)
        barra_menu.add_cascade(label="Postulante", menu=menu_postulante)

        menu_listar = tk.Menu(barra_menu, tearoff=0)
        menu_listar.add_command(label="Listar requerimientos", command=self.abrir_listar_requerimientos)
        menu_listar.add_command(label="Listar postulantes", command=self.abrir_listar_postulantes)
        barra_menu.add_cascade(label="Listar", menu=menu_listar)

        menu_acerca = tk.Menu(barra_menu, tearoff=0)
        menu_acerca.add_command(label="Información del sistema", command=self.abrir_informacion_sistema)
        menu_acerca.add_separator()
        menu_acerca.add_command(label="Salir", command=self.ventana.quit)
        barra_menu.add_cascade(label="Acerca de", menu=menu_acerca)

        self.ventana.config(menu=barra_menu)