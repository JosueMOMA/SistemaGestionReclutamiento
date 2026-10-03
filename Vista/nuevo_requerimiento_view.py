# Vista/nuevo_requerimiento_view.py
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry  # <-- Importamos el selector de fechas


class NuevoRequerimientoView:

  def __init__(self, parent):
    self.ventana = tk.Toplevel(parent)
    self.ventana.title("Registrar Requerimiento")
    self.ventana.grab_set()

    ancho_ventana = 595
    alto_ventana = 490
    ancho_pantalla = self.ventana.winfo_screenwidth()
    alto_pantalla = self.ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
    self.ventana.resizable(False, False)

    self.crear_formulario()

  def crear_formulario(self):
    main_frame = tk.Frame(self.ventana, padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Título principal centrado
    titulo = tk.Label(
        main_frame,
        text="Registrar Requerimiento",
        font=("Arial", 14, "bold"),
        anchor="center",
    )
    titulo.grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky="ew")

    # Creación de los elementos del formulario
    self.txt_id = tk.Entry(main_frame, width=25)
    self.txt_id.insert(0, "REQ-001")
    self.txt_id.config(state="readonly")

    # --- CAMPOS DE FECHA CON CALENDAR ---
    self.txt_fecha_req = DateEntry(
        main_frame,
        width=22,
        background="darkblue",
        foreground="white",
        borderwidth=2,
        date_pattern="yyyy-mm-dd",
        locale="es_ES",
    )

    self.spin_nro = tk.Spinbox(main_frame, from_=1, to=50, width=23)

    self.combo_area = ttk.Combobox(
        main_frame,
        values=[
            "Tecnología",
            "Recursos Humanos",
            "Administración",
            "Operaciones",
        ],
        width=23,
        state="readonly",
    )
    self.combo_area.current(0)

    # --- CAMPOS DE FECHA CON CALENDAR ---
    self.txt_fecha_ing = DateEntry(
        main_frame,
        width=22,
        background="darkblue",
        foreground="white",
        borderwidth=2,
        date_pattern="yyyy-mm-dd",
        locale="es_ES",
    )

    self.txt_fecha_fin = DateEntry(
        main_frame,
        width=22,
        background="darkblue",
        foreground="white",
        borderwidth=2,
        date_pattern="yyyy-mm-dd",
        locale="es_ES",
    )

    self.combo_puesto = ttk.Combobox(
        main_frame,
        values=[
            "Desarrollador Python",
            "Analista de RRHH",
            "Asistente Administrativo",
        ],
        width=23,
        state="readonly",
    )
    self.combo_puesto.current(0)

    self.combo_regimen = ttk.Combobox(
        main_frame,
        values=["CAS", "728", "Prácticas", "Locación"],
        width=23,
        state="readonly",
    )
    self.combo_regimen.current(0)

    self.combo_grado = ttk.Combobox(
        main_frame,
        values=["Secundaria completa", "Técnico", "Universitario"],
        width=23,
        state="readonly",
    )
    self.combo_grado.current(0)
    self.combo_grado.bind(
        "<<ComboboxSelected>>", self.verificar_grado_instruccion
    )

    self.combo_profesion = ttk.Combobox(
        main_frame,
        values=[
            "Ingeniería de Sistemas",
            "Administración",
            "Contabilidad",
            "Psicología",
        ],
        width=23,
        state="disabled",
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
      widget.grid(
          row=fila_base + 1, column=columna, sticky="w", padx=10, pady=(0, 6)
      )

    # --- DESCRIPCIÓN ---
    fila_desc = 9
    lbl_desc = tk.Label(
        main_frame, text="Descripción:", font=("Arial", 9, "bold")
    )
    lbl_desc.grid(
        row=fila_desc, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 2)
    )

    self.txt_descripcion = tk.Text(main_frame, width=66, height=4)
    self.txt_descripcion.grid(
        row=fila_desc + 1,
        column=0,
        columnspan=3,
        sticky="w",
        padx=10,
        pady=(0, 15),
    )

    # --- BOTONES ---
    frame_botones = tk.Frame(main_frame)
    frame_botones.grid(
        row=fila_desc + 2, column=0, columnspan=3, sticky="n", pady=10
    )

    btn_cancelar = tk.Button(
        frame_botones, text="Cancelar", width=12, command=self.ventana.destroy
    )
    btn_cancelar.pack(side=tk.LEFT, padx=10)

    btn_guardar = tk.Button(
        frame_botones,
        text="Guardar",
        width=12,
        bg="#4CAF50",
        fg="white",
        command=self.guardar_datos,
    )
    btn_guardar.pack(side=tk.LEFT, padx=10)

  def verificar_grado_instruccion(self, event):
    grado_seleccionado = self.combo_grado.get()
    if grado_seleccionado in ["Técnico", "Universitario"]:
      self.combo_profesion.config(state="readonly")
    else:
      self.combo_profesion.set("")
      self.combo_profesion.config(state="disabled")

  def guardar_datos(self):
    # Nota: Para obtener el valor de la fecha seleccionada puedes usar self.txt_fecha_req.get()
    messagebox.showinfo("Aviso", "¡Requerimiento registrado con éxito!")
    self.ventana.destroy()