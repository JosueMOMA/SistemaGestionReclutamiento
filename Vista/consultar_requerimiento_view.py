# Vista/consultar_requerimiento_view.py
import tkinter as tk
from tkinter import messagebox, ttk


class ConsultarRequerimientoView:

  def __init__(self, parent):
    self.ventana = tk.Toplevel(parent)
    self.ventana.title("Consultar Requerimiento")
    self.ventana.grab_set()

    # --- CENTRAR LA VENTANA (Diseño de 2 columnas) ---
    ancho_ventana = 515
    alto_ventana = 650
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
        text="Consultar Requerimiento",
        font=("Arial", 14, "bold"),
        anchor="center",
    )
    titulo.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="ew")

    # --- FILA DE BÚSQUEDA (ID Requerimiento + Botón Lupa) ---
    lbl_id = tk.Label(
        main_frame, text="ID Requerimiento:", font=("Arial", 9, "bold")
    )
    lbl_id.grid(row=1, column=0, sticky="w", padx=10, pady=(4, 2))

    frame_busqueda = tk.Frame(main_frame)
    frame_busqueda.grid(
        row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10)
    )

    self.txt_id = tk.Entry(frame_busqueda, width=30)
    self.txt_id.pack(side=tk.LEFT, padx=(0, 5))

    btn_buscar = tk.Button(
        frame_busqueda, text="🔍 Buscar", command=self.buscar_requerimiento
    )
    btn_buscar.pack(side=tk.LEFT)

    # --- CAMPOS DE INFORMACIÓN (No editables) ---
    # Instanciamos los campos de texto en estado "readonly"
    self.txt_fecha_req = self.crear_campo_lectura(main_frame)
    self.txt_fecha_ing = self.crear_campo_lectura(main_frame)
    self.txt_nro_req = self.crear_campo_lectura(main_frame)
    self.txt_fecha_fin = self.crear_campo_lectura(main_frame)
    self.txt_area = self.crear_campo_lectura(main_frame)
    self.txt_regimen = self.crear_campo_lectura(main_frame)
    self.txt_puesto = self.crear_campo_lectura(main_frame)
    self.txt_grado = self.crear_campo_lectura(main_frame)
    self.txt_profesion = self.crear_campo_lectura(main_frame)
    self.txt_sueldo = self.crear_campo_lectura(main_frame)
    self.txt_experiencia = self.crear_campo_lectura(main_frame)
    self.txt_postulantes = self.crear_campo_lectura(main_frame)
    self.txt_estado = self.crear_campo_lectura(main_frame)

    campos_info = [
        ("Fecha Requerimiento:", self.txt_fecha_req),
        ("Fecha Ingreso:", self.txt_fecha_ing),
        ("Nro Requeridos:", self.txt_nro_req),
        ("Fecha Fin Contrato:", self.txt_fecha_fin),
        ("Área:", self.txt_area),
        ("Régimen Laboral:", self.txt_regimen),
        ("Puesto:", self.txt_puesto),
        ("Grado Instrucción:", self.txt_grado),
        ("Profesión:", self.txt_profesion),
        ("Sueldo Base:", self.txt_sueldo),
        ("Con Experiencia:", self.txt_experiencia),
        ("Nro Postulantes:", self.txt_postulantes),
        ("Estado:", self.txt_estado),
    ]

    # Distribución en 2 columnas (empezando desde la fila 3)
    for idx, (label_text, widget) in enumerate(campos_info):
      fila_base = (idx // 2) * 2 + 3
      columna = idx % 2

      lbl = tk.Label(main_frame, text=label_text, font=("Arial", 9, "bold"))
      lbl.grid(row=fila_base, column=columna, sticky="w", padx=10, pady=(4, 2))
      widget.grid(
          row=fila_base + 1, column=columna, sticky="w", padx=10, pady=(0, 6)
      )

    # --- DESCRIPCIÓN (Ocupa las 2 columnas al final) ---
    fila_desc = 17
    lbl_desc = tk.Label(
        main_frame, text="Descripción:", font=("Arial", 9, "bold")
    )
    lbl_desc.grid(
        row=fila_desc, column=0, columnspan=2, sticky="w", padx=10, pady=(6, 2)
    )

    self.txt_descripcion = tk.Text(
        main_frame, width=56, height=3, state="disabled"
    )
    self.txt_descripcion.grid(
        row=fila_desc + 1,
        column=0,
        columnspan=2,
        sticky="w",
        padx=10,
        pady=(0, 10),
    )

    # --- BOTONES (Limpiar y Cerrar centrados) ---
    frame_botones = tk.Frame(main_frame)
    frame_botones.grid(
        row=fila_desc + 2, column=0, columnspan=2, sticky="n", pady=5
    )

    btn_limpiar = tk.Button(
        frame_botones, text="Limpiar", width=12, command=self.limpiar_campos
    )
    btn_limpiar.pack(side=tk.LEFT, padx=10)

    btn_cerrar = tk.Button(
        frame_botones, text="Cerrar", width=12, command=self.ventana.destroy
    )
    btn_cerrar.pack(side=tk.LEFT, padx=10)

  def crear_campo_lectura(self, parent):
    # Función auxiliar para crear inputs de solo lectura estandarizados
    txt = tk.Entry(parent, width=35)
    txt.config(state="readonly")
    return txt

  def buscar_requerimiento(self):
    id_req = self.txt_id.get().strip()
    if not id_req:
      messagebox.showwarning(
          "Advertencia", "Por favor ingrese un ID de requerimiento."
      )
      return

    # Simulación de datos encontrados (más adelante lo conectará el Controlador con el Modelo)
    messagebox.showinfo(
        "Búsqueda", f"Buscando requerimiento con ID: {id_req}..."
    )

  def limpiar_campos(self):
    self.txt_id.delete(0, tk.END)
    # Limpiar campos de solo lectura temporalmente habilitándolos
    campos = [
        self.txt_fecha_req,
        self.txt_fecha_ing,
        self.txt_nro_req,
        self.txt_fecha_fin,
        self.txt_area,
        self.txt_regimen,
        self.txt_puesto,
        self.txt_grado,
        self.txt_profesion,
        self.txt_sueldo,
        self.txt_experiencia,
        self.txt_postulantes,
        self.txt_estado,
    ]
    for campo in campos:
      campo.config(state="normal")
      campo.delete(0, tk.END)
      campo.config(state="readonly")

    self.txt_descripcion.config(state="normal")
    self.txt_descripcion.delete("1.0", tk.END)
    self.txt_descripcion.config(state="disabled")