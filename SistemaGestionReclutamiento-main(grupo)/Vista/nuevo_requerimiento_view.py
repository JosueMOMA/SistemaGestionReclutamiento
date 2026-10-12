import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry 
from datetime import date, timedelta
from Controlador.requerimiento_controller import RequerimientoController
from Modelo import catalogo
from Modelo.regimen_factory import RegimenFactory

class NuevoRequerimientoView:

    def __init__(self, parent, xEmpresa):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Requerimiento")
        self.ventana.grab_set()
        self.xEmpresa = xEmpresa

        ancho_ventana = 630
        alto_ventana = 490
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.ventana.resizable(False, False)

        self.crear_formulario()
        self.xControlador = RequerimientoController(xEmpresa=self.xEmpresa, xVistaNuevo=self)

    def crear_formulario(self):
        main_frame = tk.Frame(self.ventana, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        titulo = tk.Label(
            main_frame,
            text="Registrar Requerimiento",
            font=("Arial", 14, "bold"),
            anchor="center",
        )
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky="ew")

        self.txt_id = tk.Entry(main_frame, width=25)
        # ID correlativo generado por la Empresa (REQ-001, REQ-002...)
        self.txt_id.insert(0, self.xEmpresa.generar_id_requerimiento())
        self.txt_id.config(state="readonly")

        self.txt_fecha_req = DateEntry(
            main_frame, width=22, background="darkblue", foreground="white", 
            borderwidth=2, date_pattern="yyyy-mm-dd", locale="es_ES"
        )

        self.spin_nro = tk.Spinbox(main_frame, from_=1, to=50, width=23)

        self.combo_area = ttk.Combobox(
            main_frame,
            values=catalogo.obtener_areas(),
            width=23, state="readonly",
        )
        self.combo_area.current(0)
        # Al cambiar el área se actualizan los puestos disponibles
        self.combo_area.bind("<<ComboboxSelected>>", self.actualizar_puestos)

        self.txt_fecha_ing = DateEntry(
            main_frame, width=22, background="darkblue", foreground="white", 
            borderwidth=2, date_pattern="yyyy-mm-dd", locale="es_ES"
        )

        self.txt_fecha_fin = DateEntry(
            main_frame, width=22, background="darkblue", foreground="white", 
            borderwidth=2, date_pattern="yyyy-mm-dd", locale="es_ES"
        )
        # Por defecto el contrato dura 3 meses desde hoy
        self.txt_fecha_fin.set_date(date.today() + timedelta(days=90))

        self.combo_puesto = ttk.Combobox(
            main_frame,
            values=catalogo.obtener_puestos(self.combo_area.get()),
            width=23, state="readonly",
        )
        self.combo_puesto.current(0)

        self.combo_regimen = ttk.Combobox(
            main_frame, values=RegimenFactory.obtener_tipos(),
            width=23, state="readonly",
        )
        self.combo_regimen.current(0)

        self.combo_grado = ttk.Combobox(
            main_frame, values=catalogo.obtener_grados(),
            width=23, state="readonly",
        )
        self.combo_grado.current(0)
        self.combo_grado.bind("<<ComboboxSelected>>", self.verificar_grado_instruccion)

        self.combo_profesion = ttk.Combobox(
            main_frame,
            values=catalogo.obtener_profesiones(),
            width=23, state="disabled",
        )

        self.chk_experiencia_var = tk.IntVar()
        self.chk_experiencia = tk.Checkbutton(
            main_frame, text="Con experiencia", variable=self.chk_experiencia_var
        )

        campos = [
            ("ID Requerimiento:", self.txt_id),
            ("Fecha Requerimiento:", self.txt_fecha_req),
            ("Nro Requeridos:", self.spin_nro),
            ("Área:", self.combo_area),
            ("Fecha Ingreso:", self.txt_fecha_ing),
            ("Fecha Fin Contrato:", self.txt_fecha_fin),
            ("Puesto:", self.combo_puesto),
            ("Régimen Laboral:", self.combo_regimen),
            ("Grado Instrucción:", self.combo_grado),
            ("Profesión:", self.combo_profesion),
            ("Experiencia:", self.chk_experiencia),
        ]

        for idx, (label_text, widget) in enumerate(campos):
            fila_base = (idx // 3) * 2 + 1
            columna = idx % 3
            lbl = tk.Label(main_frame, text=label_text, font=("Arial", 9, "bold"))
            lbl.grid(row=fila_base, column=columna, sticky="w", padx=10, pady=(6, 2))
            widget.grid(row=fila_base + 1, column=columna, sticky="w", padx=10, pady=(0, 6))

        fila_desc = 9
        lbl_desc = tk.Label(main_frame, text="Descripción:", font=("Arial", 9, "bold"))
        lbl_desc.grid(row=fila_desc, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 2))

        self.txt_descripcion = tk.Text(main_frame, width=66, height=4, wrap="word")
        self.txt_descripcion.grid(
            row=fila_desc + 1, column=0, columnspan=3, sticky="w", padx=10, pady=(0, 15)
        )

        frame_botones = tk.Frame(main_frame)
        frame_botones.grid(row=fila_desc + 2, column=0, columnspan=3, sticky="n", pady=10)

        btn_cancelar = tk.Button(
            frame_botones, text="Cancelar", width=12, command=self.ventana.destroy
        )
        btn_cancelar.pack(side=tk.LEFT, padx=10)

        btn_guardar = tk.Button(
            frame_botones, text="Guardar", width=12, bg="#4CAF50", fg="white", 
            command=self.guardar_datos
        )
        btn_guardar.pack(side=tk.LEFT, padx=10)

    def actualizar_puestos(self, event):
        # Cargamos solo los puestos que pertenecen al área seleccionada
        xPuestos = catalogo.obtener_puestos(self.combo_area.get())
        self.combo_puesto["values"] = xPuestos
        if xPuestos:
            self.combo_puesto.current(0)
        else:
            self.combo_puesto.set("")

    def verificar_grado_instruccion(self, event):
        grado_seleccionado = self.combo_grado.get()
        if grado_seleccionado in ["Técnico", "Universitario"]:
            self.combo_profesion.config(state="readonly")
        else:
            self.combo_profesion.set("")
            self.combo_profesion.config(state="disabled")

    def guardar_datos(self):
        self.xControlador.xRegistrarRequerimiento()