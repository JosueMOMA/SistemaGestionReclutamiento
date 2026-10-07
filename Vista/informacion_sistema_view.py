import tkinter as tk


class InformacionSistemaView:

  def __init__(self, parent):
    self.ventana = tk.Toplevel(parent)
    self.ventana.title("Acerca de | Información del Sistema")
    self.ventana.grab_set()

    # --- CENTRAR LA VENTANA ---
    ancho_ventana = 400
    alto_ventana = 440
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
        text="Sistema de Gestión de Reclutamiento\nSISGER v1.0",
        font=("Arial", 14, "bold"),
        justify="center",
    )
    titulo.pack(pady=(5, 15))

    # --- DOCENTE ---
    tk.Label(main_frame, text="DOCENTE", font=("Arial", 10, "bold")).pack(
        pady=(0, 5)
    )
    tk.Label(
        main_frame, text="César Eduardo Chahuas Rebatta", font=("Arial", 10)
    ).pack(pady=2)

    # --- INTEGRANTES ---
    tk.Label(main_frame, text="Integrantes", font=("Arial", 10, "bold")).pack(
        pady=(15, 5)
    )
    integrantes = [
        "Gomez Huaman Daniel Luis Humberto",
        "Licapa Infanzon, Gianfranco",
        "Moreno Martinez Josue Aarom",
        "Mertz Acero Angel Matias",
    ]
    for nombre in integrantes:
      tk.Label(main_frame, text=nombre, font=("Arial", 10)).pack(pady=2)

    # --- FECHA ---
    tk.Label(
        main_frame, text="Setiembre 2026", font=("Arial", 10, "bold")
    ).pack(pady=(20, 10))

    # --- BOTÓN Gracias ---
    btn_gracias = tk.Button(
        main_frame, text="Gracias", width=12, command=self.ventana.destroy
    )
    btn_gracias.pack(pady=5)