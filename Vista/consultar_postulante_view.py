# Vista/consultar_postulante_view.py
import tkinter as tk
from tkinter import messagebox, ttk


class ConsultarPostulanteView:

  def __init__(self, parent):
    self.ventana = tk.Toplevel(parent)
    self.ventana.title("Consultar Postulante")
    self.ventana.grab_set()

    # --- CENTRAR LA VENTANA (Diseño de 2 columnas) ---
    ancho_ventana = 510
    alto_ventana = 520
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
        text="Consultar Postulante",
        font=("Arial", 14, "bold"),
        anchor="center",
    )
    titulo.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="ew")

    # --- FILA DE BÚSQUEDA (ID Postulante + Botón Lupa) ---
    lbl_id = tk.Label(
        main_frame, text="ID Postulante:", font=("Arial", 9, "bold")
    )
    lbl_id.grid(row=1, column=0, sticky="w", padx=10, pady=(4, 2))

    frame_busqueda = tk.Frame(main_frame)
    frame_busqueda.grid(
        row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 15)
    )

    self.txt_id = tk.Entry(frame_busqueda, width=30)
    self.txt_id.pack(side=tk.LEFT, padx=(0, 5))

    btn_buscar = tk.Button(
        frame_busqueda, text="🔍 Buscar", command=self.buscar_postulante
    )
    btn_buscar.pack(side=tk.LEFT)

    # --- CAMPOS DE INFORMACIÓN (No editables) ---
    self.txt_ape_pat = self.crear_campo_lectura(main_frame)
    self.txt_ape_mat = self.crear_campo_lectura(main_frame)
    self.txt_nombres = self.crear_campo_lectura(main_frame)
    self.txt_fecha_post = self.crear_campo_lectura(main_frame)
    self.txt_celular = self.crear_campo_lectura(main_frame)
    self.txt_edad = self.crear_campo_lectura(main_frame)
    self.txt_area = self.crear_campo_lectura(main_frame)
    self.txt_puesto = self.crear_campo_lectura(main_frame)
    self.txt_regimen = self.crear_campo_lectura(main_frame)
    self.txt_sueldo_base = self.crear_campo_lectura(main_frame)
    self.txt_descuento = self.crear_campo_lectura(main_frame)
    self.txt_sueldo_neto = self.crear_campo_lectura(main_frame)

    campos_info = [
        ("Apellido Paterno:", self.txt_ape_pat),
        ("Apellido Materno:", self.txt_ape_mat),
        ("Nombres:", self.txt_nombres),
        ("Fecha Postulación:", self.txt_fecha_post),
        ("Celular:", self.txt_celular),
        ("Edad:", self.txt_edad),
        ("Área:", self.txt_area),
        ("Puesto:", self.txt_puesto),
        ("Régimen Laboral:", self.txt_regimen),
        ("Sueldo Base:", self.txt_sueldo_base),
        ("Descuento:", self.txt_descuento),
        ("Sueldo Neto:", self.txt_sueldo_neto),
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

    # --- BOTONES (Limpiar y Cerrar centrados) ---
    fila_botones = 15
    frame_botones = tk.Frame(main_frame)
    frame_botones.grid(
        row=fila_botones, column=0, columnspan=2, sticky="", pady=15
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
    txt = tk.Entry(parent, width=35)
    txt.config(state="readonly")
    return txt

  def buscar_postulante(self):
    id_post = self.txt_id.get().strip()
    if not id_post:
      messagebox.showwarning(
          "Advertencia", "Por favor ingrese un ID de postulante."
      )
      return
    messagebox.showinfo(
        "Búsqueda", f"Buscando postulante con ID: {id_post}..."
    )

  def limpiar_campos(self):
    self.txt_id.delete(0, tk.END)
    campos = [
        self.txt_ape_pat,
        self.txt_ape_mat,
        self.txt_nombres,
        self.txt_fecha_post,
        self.txt_celular,
        self.txt_edad,
        self.txt_area,
        self.txt_puesto,
        self.txt_regimen,
        self.txt_sueldo_base,
        self.txt_descuento,
        self.txt_sueldo_neto,
    ]
    for campo in campos:
      campo.config(state="normal")
      campo.delete(0, tk.END)
      campo.config(state="readonly")