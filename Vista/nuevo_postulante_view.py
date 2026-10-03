# Vista/nuevo_postulante_view.py
from datetime import date
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry


class NuevoPostulanteView:

  def __init__(self, parent):
    self.ventana = tk.Toplevel(parent)
    self.ventana.title("Registrar Postulante")
    self.ventana.grab_set()

    # --- CENTRAR LA VENTANA ---
    ancho_ventana = 600
    alto_ventana = 680
    ancho_pantalla = self.ventana.winfo_screenwidth()
    alto_pantalla = self.ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
    self.ventana.resizable(False, False)

    self.crear_formulario()

  def crear_formulario(self):
    main_frame = tk.Frame(self.ventana, padx=15, pady=15)
    main_frame.pack(fill=tk.BOTH, expand=True)

# --- CABECERA (Título perfectamente centrado y ID/Fecha a la derecha) ---
    header_frame = tk.Frame(main_frame, height=55)
    header_frame.pack(fill=tk.X, pady=(0, 10))
    header_frame.pack_propagate(
        False
    )  # Mantiene una altura fija para el contenedor

    # Título centrado de forma absoluta en el contenedor
    titulo = tk.Label(
        header_frame, text="Registrar Postulante", font=("Arial", 14, "bold")
    )
    titulo.place(relx=0.5, rely=0.5, anchor="center")

    # Contenedor derecho para ID y Fecha
    info_derecha_frame = tk.Frame(header_frame)
    info_derecha_frame.place(relx=1.0, rely=0.5, anchor="e")

    # ID Postulante
    tk.Label(
        info_derecha_frame,  font=("Arial", 8, "bold")
    ).grid(row=0, column=0, sticky="e", padx=5)
    self.txt_id = tk.Entry(info_derecha_frame, width=15)
    self.txt_id.insert(0, "POST-001")
    self.txt_id.config(state="readonly")
    self.txt_id.grid(row=0, column=1, sticky="w", pady=2)

    # Fecha de Postulación
    tk.Label(
        info_derecha_frame,
        
        font=("Arial", 8, "bold"),
    ).grid(row=1, column=0, sticky="e", padx=5)
    self.txt_fecha_post = tk.Entry(info_derecha_frame, width=15)
    self.txt_fecha_post.insert(0, date.today().strftime("%Y-%m-%d"))
    self.txt_fecha_post.config(state="readonly")
    self.txt_fecha_post.grid(row=1, column=1, sticky="w", pady=2)

    # --- 1. GROUP BOX: DATOS PERSONALES (3 columnas) ---
    gb_personales = tk.LabelFrame(
        main_frame,
        text=" Datos Personales ",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=10,
    )
    gb_personales.pack(fill=tk.X, pady=(0, 10))

    self.txt_dni = tk.Entry(gb_personales, width=25)
    self.txt_ape_pat = tk.Entry(gb_personales, width=25)
    self.txt_ape_mat = tk.Entry(gb_personales, width=25)
    self.txt_nombres = tk.Entry(gb_personales, width=25)

    self.combo_sexo = ttk.Combobox(
        gb_personales,
        values=["Masculino", "Femenino", "Otro"],
        width=23,
        state="readonly",
    )
    self.combo_sexo.current(0)

    self.combo_estado_civil = ttk.Combobox(
        gb_personales,
        values=["Soltero(a)", "Casado(a)", "Divorciado(a)", "Viudo(a)"],
        width=23,
        state="readonly",
    )
    self.combo_estado_civil.current(0)

    self.date_nacimiento = DateEntry(
        gb_personales,
        width=22,
        background="darkblue",
        foreground="white",
        borderwidth=2,
        date_pattern="yyyy-mm-dd",
        locale="es_ES",
    )

    self.txt_celular = tk.Entry(gb_personales, width=25)
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
      tk.Label(
          gb_personales, text=lbl_txt, font=("Arial", 8, "bold")
      ).grid(row=r, column=c, sticky="w", padx=8, pady=(2, 0))
      widget.grid(row=r + 1, column=c, sticky="w", padx=8, pady=(0, 5))

    # --- 2. GROUP BOX: DATOS DE DIRECCIÓN (3 columnas, dirección ocupa largo de 3) ---
    gb_direccion = tk.LabelFrame(
        main_frame,
        text=" Datos de Dirección ",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=10,
    )
    gb_direccion.pack(fill=tk.X, pady=(0, 10))

    self.combo_dep = ttk.Combobox(
        gb_direccion,
        values=["Lima", "Arequipa", "La Libertad", "Piura"],
        width=23,
        state="readonly",
    )
    self.combo_dep.current(0)

    self.combo_prov = ttk.Combobox(
        gb_direccion,
        values=["Lima", "Callao", "Arequipa"],
        width=23,
        state="readonly",
    )
    self.combo_prov.current(0)

    self.combo_dist = ttk.Combobox(
        gb_direccion,
        values=["Miraflores", "San Isidro", "Surco", "Lima"],
        width=23,
        state="readonly",
    )
    self.combo_dist.current(0)

    self.txt_direccion = tk.Entry(gb_direccion, width=86)

    # Fila 1: Dep, Prov, Dist
    tk.Label(
        gb_direccion, text="Departamento:", font=("Arial", 8, "bold")
    ).grid(row=0, column=0, sticky="w", padx=8, pady=(2, 0))
    self.combo_dep.grid(row=1, column=0, sticky="w", padx=8, pady=(0, 5))

    tk.Label(gb_direccion, text="Provincia:", font=("Arial", 8, "bold")).grid(
        row=0, column=1, sticky="w", padx=8, pady=(2, 0)
    )
    self.combo_prov.grid(row=1, column=1, sticky="w", padx=8, pady=(0, 5))

    tk.Label(gb_direccion, text="Distrito:", font=("Arial", 8, "bold")).grid(
        row=0, column=2, sticky="w", padx=8, pady=(2, 0)
    )
    self.combo_dist.grid(row=1, column=2, sticky="w", padx=8, pady=(0, 5))

    # Fila 2: Dirección (Abarca las 3 columnas)
    tk.Label(gb_direccion, text="Dirección:", font=("Arial", 8, "bold")).grid(
        row=2, column=0, sticky="w", padx=8, pady=(2, 0)
    )
    self.txt_direccion.grid(
        row=3, column=0, columnspan=3, sticky="w", padx=8, pady=(0, 5)
    )

    # --- 3. GROUP BOX: DATOS DE EDUCACIÓN (3 columnas) ---
    gb_educacion = tk.LabelFrame(
        main_frame,
        text=" Datos de Educación ",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=10,
    )
    gb_educacion.pack(fill=tk.X, pady=(0, 10))

    self.combo_grado = ttk.Combobox(
        gb_educacion,
        values=["Secundaria completa", "Técnico", "Universitario"],
        width=23,
        state="readonly",
    )
    self.combo_grado.current(0)
    self.combo_grado.bind(
        "<<ComboboxSelected>>", self.verificar_grado_instruccion
    )

    self.combo_profesion = ttk.Combobox(
        gb_educacion,
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
        gb_educacion,
        text="Cuenta con experiencia",
        variable=self.chk_experiencia_var,
    )

    tk.Label(
        gb_educacion, text="Grado de Instrucción:", font=("Arial", 8, "bold")
    ).grid(row=0, column=0, sticky="w", padx=8, pady=(2, 0))
    self.combo_grado.grid(row=1, column=0, sticky="w", padx=8, pady=(0, 5))

    tk.Label(gb_educacion, text="Profesión:", font=("Arial", 8, "bold")).grid(
        row=0, column=1, sticky="w", padx=8, pady=(2, 0)
    )
    self.combo_profesion.grid(row=1, column=1, sticky="w", padx=8, pady=(0, 5))

    tk.Label(gb_educacion, text="Experiencia:", font=("Arial", 8, "bold")).grid(
        row=0, column=2, sticky="w", padx=8, pady=(2, 0)
    )
    self.chk_experiencia.grid(row=1, column=2, sticky="w", padx=8, pady=(0, 5))

    # --- 4 Y 5. DOS GROUP BOXES LADO A LADO (AFP y Postulación) ---
    bottom_boxes_frame = tk.Frame(main_frame)
    bottom_boxes_frame.pack(fill=tk.X, pady=(0, 10))

    # Izquierda: AFP
    gb_afp = tk.LabelFrame(
        bottom_boxes_frame,
        text=" Sistema de Pensiones ",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=10,
    )
    gb_afp.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

    tk.Label(gb_afp, text="Tipo de AFP:", font=("Arial", 8, "bold")).pack(
        anchor="w", padx=5, pady=(2, 0)
    )
    self.combo_afp = ttk.Combobox(
        gb_afp,
        values=["AFP Integra", "AFP Habitat", "AFP Prima", "AFP Profuturo", "ONP"],
        width=35,
        state="readonly",
    )
    self.combo_afp.pack(anchor="w", padx=5, pady=(0, 5))
    self.combo_afp.current(0)

    # Derecha: Postulación
    gb_postulacion = tk.LabelFrame(
        bottom_boxes_frame,
        text=" Postulación ",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=10,
    )
    gb_postulacion.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

    tk.Label(
        gb_postulacion,
        text="ID Requerimiento:",
        font=("Arial", 8, "bold"),
    ).pack(anchor="w", padx=5, pady=(2, 0))
    self.combo_req = ttk.Combobox(
        gb_postulacion,
        values=["REQ-001 - Desarrollador Python", "REQ-002 - Analista RRHH"],
        width=35,
        state="readonly",
    )
    self.combo_req.pack(anchor="w", padx=5, pady=(0, 5))
    self.combo_req.current(0)

    # --- BOTONES (Cancelar y Guardar centrados) ---
    frame_botones = tk.Frame(main_frame)
    frame_botones.pack(pady=5)

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
    messagebox.showinfo("Aviso", "¡Postulante registrado con éxito!")
    self.ventana.destroy()