from datetime import date
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from Controlador.postulante_controller import PostulanteController
from Modelo.catalogos import AFP_DESCUENTOS, PROFESIONES, UBICACIONES

class NuevoPostulanteView:

    def __init__(self, parent, xEmpresa):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Postulante")
        self.ventana.grab_set()
        self.xEmpresa = xEmpresa

        ancho_ventana = 600
        alto_ventana = 680
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.ventana.resizable(False, False)

        self.crear_formulario()
        
        # Cargar los requerimientos activos en el combobox
        reqs_disponibles = [
            f"{req.id_proceso} - {req.area.puesto.nombre_puesto}"
            for req in self.xEmpresa.lista_requerimientos
            if req.estado_requerimiento == "Activo"
        ]
        if reqs_disponibles:
            self.combo_req['values'] = reqs_disponibles
            self.combo_req.current(0)
            
        self.xControlador = PostulanteController(xEmpresa=self.xEmpresa, xVistaNuevo=self)

    def crear_formulario(self):
        main_frame = tk.Frame(self.ventana, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        validar_nombre = (
            self.ventana.register(self._permitir_solo_letras_y_espacios)
        )

        header_frame = tk.Frame(main_frame, height=55)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        titulo = tk.Label(header_frame, text="Registrar Postulante", font=("Arial", 14, "bold"))
        titulo.place(relx=0.5, rely=0.5, anchor="center")

        info_derecha_frame = tk.Frame(header_frame)
        info_derecha_frame.place(relx=1.0, rely=0.5, anchor="e")

        tk.Label(info_derecha_frame, font=("Arial", 8, "bold")).grid(row=0, column=0, sticky="e", padx=5)
        self.txt_id = tk.Entry(info_derecha_frame, width=15)
        self.txt_id.insert(0, self.xEmpresa.siguiente_id_postulante())
        self.txt_id.config(state="readonly")
        self.txt_id.grid(row=0, column=1, sticky="w", pady=2)

        tk.Label(info_derecha_frame, font=("Arial", 8, "bold")).grid(row=1, column=0, sticky="e", padx=5)
        self.txt_fecha_post = tk.Entry(info_derecha_frame, width=15)
        self.txt_fecha_post.insert(0, date.today().strftime("%Y-%m-%d"))
        self.txt_fecha_post.config(state="readonly")
        self.txt_fecha_post.grid(row=1, column=1, sticky="w", pady=2)

        gb_personales = tk.LabelFrame(main_frame, text=" Datos Personales ", font=("Arial", 10, "bold"), padx=10, pady=10)
        gb_personales.pack(fill=tk.X, pady=(0, 10))

        validar_dni = self.ventana.register(self._permitir_digitos_hasta)
        validar_celular = self.ventana.register(self._permitir_digitos_hasta)
        opciones_dni = {
            "validate": "key",
            "validatecommand": (validar_dni, "%P", "8"),
        }
        opciones_celular = {
            "validate": "key",
            "validatecommand": (validar_celular, "%P", "9"),
        }
        self.txt_dni = tk.Entry(gb_personales, width=25, **opciones_dni)
        opciones_nombre = {
            "validate": "key",
            "validatecommand": (validar_nombre, "%P"),
        }
        self.txt_ape_pat = tk.Entry(gb_personales, width=25, **opciones_nombre)
        self.txt_ape_mat = tk.Entry(gb_personales, width=25, **opciones_nombre)
        self.txt_nombres = tk.Entry(gb_personales, width=25, **opciones_nombre)

        self.combo_sexo = ttk.Combobox(gb_personales, values=["Masculino", "Femenino", "Otro"], width=23, state="readonly")
        self.combo_sexo.current(0)

        self.combo_estado_civil = ttk.Combobox(gb_personales, values=["Soltero(a)", "Casado(a)", "Divorciado(a)", "Viudo(a)"], width=23, state="readonly")
        self.combo_estado_civil.current(0)

        self.date_nacimiento = DateEntry(gb_personales, width=22, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd", locale="es_ES")

        self.txt_celular = tk.Entry(gb_personales, width=25, **opciones_celular)
        self.txt_correo = tk.Entry(gb_personales, width=25)

        campos_personales = [
            ("DNI:", self.txt_dni),
            ("Apellido Paterno:", self.txt_ape_pat),
            ("Apellido Materno:", self.txt_ape_mat),
            ("Nombres:", self.txt_nombres),
            ("Sexo:", self.combo_sexo),
            ("Estado Civil:", self.combo_estado_civil),
            ("Fecha de Nacimiento:", self.date_nacimiento),
            ("Celular:", self.txt_celular),
            ("Correo Electrónico:", self.txt_correo),
        ]

        for idx, (lbl_txt, widget) in enumerate(campos_personales):
            r = (idx // 3) * 2
            c = idx % 3
            tk.Label(gb_personales, text=lbl_txt, font=("Arial", 8, "bold")).grid(row=r, column=c, sticky="w", padx=8, pady=(2, 0))
            widget.grid(row=r + 1, column=c, sticky="w", padx=8, pady=(0, 5))

        gb_direccion = tk.LabelFrame(main_frame, text=" Datos de Dirección ", font=("Arial", 10, "bold"), padx=10, pady=10)
        gb_direccion.pack(fill=tk.X, pady=(0, 10))

        self.combo_dep = ttk.Combobox(gb_direccion, values=list(UBICACIONES), width=23, state="readonly")
        self.combo_dep.current(0)
        self.combo_dep.bind("<<ComboboxSelected>>", self.actualizar_provincias)

        self.combo_prov = ttk.Combobox(gb_direccion, values=[], width=23, state="readonly")
        self.combo_prov.bind("<<ComboboxSelected>>", self.actualizar_distritos)

        self.combo_dist = ttk.Combobox(gb_direccion, values=[], width=23, state="readonly")

        self.txt_direccion = tk.Entry(gb_direccion, width=86)

        tk.Label(gb_direccion, text="Departamento:", font=("Arial", 8, "bold")).grid(row=0, column=0, sticky="w", padx=8, pady=(2, 0))
        self.combo_dep.grid(row=1, column=0, sticky="w", padx=8, pady=(0, 5))

        tk.Label(gb_direccion, text="Provincia:", font=("Arial", 8, "bold")).grid(row=0, column=1, sticky="w", padx=8, pady=(2, 0))
        self.combo_prov.grid(row=1, column=1, sticky="w", padx=8, pady=(0, 5))

        tk.Label(gb_direccion, text="Distrito:", font=("Arial", 8, "bold")).grid(row=0, column=2, sticky="w", padx=8, pady=(2, 0))
        self.combo_dist.grid(row=1, column=2, sticky="w", padx=8, pady=(0, 5))

        tk.Label(gb_direccion, text="Dirección:", font=("Arial", 8, "bold")).grid(row=2, column=0, sticky="w", padx=8, pady=(2, 0))
        self.txt_direccion.grid(row=3, column=0, columnspan=3, sticky="w", padx=8, pady=(0, 5))

        gb_educacion = tk.LabelFrame(main_frame, text=" Datos de Educación ", font=("Arial", 10, "bold"), padx=10, pady=10)
        gb_educacion.pack(fill=tk.X, pady=(0, 10))

        self.combo_grado = ttk.Combobox(gb_educacion, values=["Secundaria completa", "Técnico", "Universitario"], width=23, state="readonly")
        self.combo_grado.current(0)
        self.combo_grado.bind("<<ComboboxSelected>>", self.verificar_grado_instruccion)

        self.combo_profesion = ttk.Combobox(gb_educacion, values=[], width=23, state="disabled")

        self.chk_experiencia_var = tk.IntVar()
        self.chk_experiencia = tk.Checkbutton(gb_educacion, text="Cuenta con experiencia", variable=self.chk_experiencia_var)

        tk.Label(gb_educacion, text="Grado de Instrucción:", font=("Arial", 8, "bold")).grid(row=0, column=0, sticky="w", padx=8, pady=(2, 0))
        self.combo_grado.grid(row=1, column=0, sticky="w", padx=8, pady=(0, 5))

        tk.Label(gb_educacion, text="Profesión:", font=("Arial", 8, "bold")).grid(row=0, column=1, sticky="w", padx=8, pady=(2, 0))
        self.combo_profesion.grid(row=1, column=1, sticky="w", padx=8, pady=(0, 5))

        tk.Label(gb_educacion, text="Experiencia:", font=("Arial", 8, "bold")).grid(row=0, column=2, sticky="w", padx=8, pady=(2, 0))
        self.chk_experiencia.grid(row=1, column=2, sticky="w", padx=8, pady=(0, 5))

        bottom_boxes_frame = tk.Frame(main_frame)
        bottom_boxes_frame.pack(fill=tk.X, pady=(0, 10))

        gb_afp = tk.LabelFrame(bottom_boxes_frame, text=" Sistema de Pensiones ", font=("Arial", 10, "bold"), padx=10, pady=10)
        gb_afp.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        tk.Label(gb_afp, text="Tipo de AFP:", font=("Arial", 8, "bold")).pack(anchor="w", padx=5, pady=(2, 0))
        self.combo_afp = ttk.Combobox(
            gb_afp,
            values=list(AFP_DESCUENTOS),
            width=35,
            state="readonly",
        )
        self.combo_afp.pack(anchor="w", padx=5, pady=(0, 5))
        self.combo_afp.current(0)

        gb_postulacion = tk.LabelFrame(bottom_boxes_frame, text=" Postulación ", font=("Arial", 10, "bold"), padx=10, pady=10)
        gb_postulacion.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        tk.Label(gb_postulacion, text="ID Requerimiento:", font=("Arial", 8, "bold")).pack(anchor="w", padx=5, pady=(2, 0))
        self.combo_req = ttk.Combobox(gb_postulacion, values=[], width=35, state="readonly")
        self.combo_req.pack(anchor="w", padx=5, pady=(0, 5))

        self.actualizar_provincias()

        frame_botones = tk.Frame(main_frame)
        frame_botones.pack(pady=5)

        btn_cancelar = tk.Button(frame_botones, text="Cancelar", width=12,bg="#A3A3A3", command=self.ventana.destroy)
        btn_cancelar.pack(side=tk.LEFT, padx=10)

        btn_guardar = tk.Button(frame_botones, text="Guardar", width=12, bg="#4C7FAF", fg="white", command=self.guardar_datos)
        btn_guardar.pack(side=tk.LEFT, padx=10)

    def verificar_grado_instruccion(self, _event):
        grado_seleccionado = self.combo_grado.get()
        if grado_seleccionado in PROFESIONES:
            self.combo_profesion["values"] = PROFESIONES[grado_seleccionado]
            self.combo_profesion.current(0)
            self.combo_profesion.config(state="readonly")
        else:
            self.combo_profesion.set("")
            self.combo_profesion.config(state="disabled")

    @staticmethod
    def _permitir_solo_letras_y_espacios(valor_propuesto):
        """Permite edición normal, pero bloquea números y símbolos desde la UI."""
        return all(caracter.isalpha() or caracter.isspace() for caracter in valor_propuesto)

    @staticmethod
    def _permitir_digitos_hasta(valor_propuesto, maximo):
        """Permite borrar y escribir únicamente dígitos hasta el límite indicado."""
        return valor_propuesto == "" or (
            valor_propuesto.isdigit() and len(valor_propuesto) <= int(maximo)
        )

    def actualizar_provincias(self, _event=None):
        provincias = list(UBICACIONES.get(self.combo_dep.get(), {}))
        self.combo_prov["values"] = provincias
        if provincias:
            self.combo_prov.current(0)
        self.actualizar_distritos()

    def actualizar_distritos(self, _event=None):
        distritos = UBICACIONES.get(self.combo_dep.get(), {}).get(self.combo_prov.get(), [])
        self.combo_dist["values"] = distritos
        if distritos:
            self.combo_dist.current(0)

    def guardar_datos(self):
        self.xControlador.xRegistrarPostulante()