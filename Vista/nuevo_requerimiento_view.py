import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry 
from Controlador.requerimiento_controller import RequerimientoController
from Modelo.catalogos import PROFESIONES, PUESTOS_POR_AREA_Y_GRADO, REGIMENES

class NuevoRequerimientoView:

    def __init__(self, parent, xEmpresa):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Requerimiento")
        self.ventana.grab_set()
        self.xEmpresa = xEmpresa

        ancho_ventana = 595
        alto_ventana = 540
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
        self.txt_id.insert(0, self.xEmpresa.siguiente_id_requerimiento())
        self.txt_id.config(state="readonly")

        self.txt_fecha_req = DateEntry(
            main_frame, width=22, background="darkblue", foreground="white", 
            borderwidth=2, date_pattern="yyyy-mm-dd", locale="es_ES"
        )

        self.spin_nro = tk.Spinbox(main_frame, from_=1, to=50, width=23)

        self.combo_area = ttk.Combobox(
            main_frame,
            values=list(PUESTOS_POR_AREA_Y_GRADO),
            width=23, state="readonly",
        )
        self.combo_area.current(0)
        self.combo_area.bind("<<ComboboxSelected>>", self.actualizar_puestos)

        self.txt_fecha_ing = DateEntry(
            main_frame, width=22, background="darkblue", foreground="white", 
            borderwidth=2, date_pattern="yyyy-mm-dd", locale="es_ES"
        )

        self.txt_fecha_fin = DateEntry(
            main_frame, width=22, background="darkblue", foreground="white", 
            borderwidth=2, date_pattern="yyyy-mm-dd", locale="es_ES"
        )

        self.combo_puesto = ttk.Combobox(
            main_frame,
            values=[],
            width=23, state="readonly",
        )
        self.combo_puesto.bind("<<ComboboxSelected>>", self.actualizar_sueldo)

        self.combo_regimen = ttk.Combobox(
            main_frame, values=list(REGIMENES),
            width=23, state="readonly",
        )
        self.combo_regimen.current(0)

        self.combo_grado = ttk.Combobox(
            main_frame, values=["Secundaria completa", "Técnico", "Universitario"],
            width=23, state="readonly",
        )
        self.combo_grado.current(0)
        self.combo_grado.bind("<<ComboboxSelected>>", self.verificar_grado_instruccion)

        self.combo_profesion = ttk.Combobox(
            main_frame,
            values=PROFESIONES["Técnico"],
            width=23, state="disabled",
        )

        self.chk_experiencia_var = tk.IntVar()
        self.chk_experiencia = tk.Checkbutton(
            main_frame, text="Con experiencia", variable=self.chk_experiencia_var
        )

        self.actualizar_puestos()

        campos = [
            ("ID Requerimiento:", self.txt_id),
            ("Fecha Requerimiento:", self.txt_fecha_req),
            ("Nro Requeridos:", self.spin_nro),
            ("Área:", self.combo_area),
            ("Fecha Ingreso:", self.txt_fecha_ing),
            ("Fecha Fin Contrato:", self.txt_fecha_fin),
            ("Grado Instrucción:", self.combo_grado),
            ("Régimen Laboral:", self.combo_regimen),
            ("Puesto:", self.combo_puesto),
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

        self.txt_descripcion = tk.Text(main_frame, width=66, height=4)
        self.txt_descripcion.grid(
            row=fila_desc + 1, column=0, columnspan=3, sticky="w", padx=10, pady=(0, 15)
        )

        frame_botones = tk.Frame(main_frame)
        frame_botones.grid(row=fila_desc + 2, column=0, columnspan=3, sticky="n", pady=10)

        btn_cancelar = tk.Button(
            frame_botones, text="Cancelar", width=12,bg="#A3A3A3", command=self.ventana.destroy
        )
        btn_cancelar.pack(side=tk.LEFT, padx=10)

        btn_guardar = tk.Button(
            frame_botones, text="Guardar", width=12, bg="#4C7FAF", fg="white", 
            command=self.guardar_datos
        )
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
        self.actualizar_puestos()

    def actualizar_puestos(self, _event=None):
        area = self.combo_area.get()
        grado = self.combo_grado.get()
        puestos = [
            nombre
            for nombre, _ in PUESTOS_POR_AREA_Y_GRADO.get(area, {}).get(grado, [])
        ]
        self.combo_puesto["values"] = puestos
        if puestos:
            self.combo_puesto.current(0)
        else:
            self.combo_puesto.set("")

    def actualizar_sueldo(self, _event=None):
        """Mantiene el evento disponible para mostrar el sueldo en futuras mejoras."""

    def guardar_datos(self):
        self.xControlador.xRegistrarRequerimiento()