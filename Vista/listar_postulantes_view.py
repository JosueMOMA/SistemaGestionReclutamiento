import tkinter as tk
from tkinter import ttk


class ListarPostulantesView:

  def __init__(self, parent, registros=None):
    self.ventana = tk.Toplevel(parent)
    self.ventana.title("Listar | Listar Postulantes")
    self.ventana.grab_set()

    # --- CENTRAR LA VENTANA ---
    ancho_ventana = 740
    alto_ventana = 380
    ancho_pantalla = self.ventana.winfo_screenwidth()
    alto_pantalla = self.ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
    self.ventana.resizable(False, False)

    self.crear_formulario()
    self.cargar_datos(registros or [])

  def crear_formulario(self):
    main_frame = tk.Frame(self.ventana, padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Título principal centrado
    titulo = tk.Label(
        main_frame,
        text="Lista de Postulantes",
        font=("Arial", 16, "bold"),
        anchor="center",
    )
    titulo.pack(pady=(10, 20))

    # --- TABLA ---
    columnas = (
        "ID Postulante",
        "Fecha Registro",
        "DNI",
        "Area",
        "Puesto",
        "Estado",
    )
    anchos = (95, 100, 90, 130, 130, 150)

    self.tabla = ttk.Treeview(
        main_frame, columns=columnas, show="headings", height=4
    )
    for col, ancho in zip(columnas, anchos):
      self.tabla.heading(col, text=col)
      self.tabla.column(col, width=ancho, anchor="center")
    self.tabla.pack()

    # --- BOTÓN Cerrar ---
    frame_botones = tk.Frame(main_frame)
    frame_botones.pack(pady=30)

    btn_cerrar = tk.Button(
        frame_botones, text="Cerrar", width=12, command=self.ventana.destroy
    )
    btn_cerrar.pack()

  def cargar_datos(self, registros):
    """Carga las filas en la tabla.

    Cada registro debe ser una tupla o lista con este orden:
    (ID Postulante, Fecha Registro, DNI, Area, Puesto, Estado)
    """
    self.tabla.delete(*self.tabla.get_children())
    for fila in registros:
      self.tabla.insert("", tk.END, values=fila)