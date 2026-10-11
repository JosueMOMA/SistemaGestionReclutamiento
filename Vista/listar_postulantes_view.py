import tkinter as tk
from tkinter import ttk

class ListarPostulantesView:

    def __init__(self, xParent, xRegistros=None):
        self.ventana = tk.Toplevel(xParent)
        self.ventana.title("Listar | Listar Postulantes")
        self.ventana.grab_set()

        # --- CENTRAR LA VENTANA ---
        xAnchoVentana = 740
        xAltoVentana = 380
        xAnchoPantalla = self.ventana.winfo_screenwidth()
        xAltoPantalla = self.ventana.winfo_screenheight()
        xPosX = (xAnchoPantalla // 2) - (xAnchoVentana // 2)
        xPosY = (xAltoPantalla // 2) - (xAltoVentana // 2)
        self.ventana.geometry(f"{xAnchoVentana}x{xAltoVentana}+{xPosX}+{xPosY}")
        self.ventana.resizable(False, False)

        self.crear_formulario()
        self.cargar_datos(xRegistros or [])

    def crear_formulario(self):
        xMainFrame = tk.Frame(self.ventana, padx=20, pady=20)
        xMainFrame.pack(fill=tk.BOTH, expand=True)

        # Título principal centrado
        xTitulo = tk.Label(
            xMainFrame,
            text="Lista de Postulantes",
            font=("Arial", 16, "bold"),
            anchor="center",
        )
        xTitulo.pack(pady=(10, 20))

        # --- TABLA ---
        xColumnas = (
            "ID Postulante",
            "Fecha Registro",
            "DNI",
            "Area",
            "Puesto",
            "Estado",
        )
        xAnchos = (95, 100, 90, 130, 130, 150)

        self.tabla = ttk.Treeview(
            xMainFrame, columns=xColumnas, show="headings", height=4
        )
        for xCol, xAncho in zip(xColumnas, xAnchos):
            self.tabla.heading(xCol, text=xCol)
            self.tabla.column(xCol, width=xAncho, anchor="center")
        self.tabla.pack()

        # --- BOTÓN Cerrar ---
        xFrameBotones = tk.Frame(xMainFrame)
        xFrameBotones.pack(pady=30)

        xBtnCerrar = tk.Button(
            xFrameBotones, text="Cerrar", width=12, command=self.ventana.destroy
        )
        xBtnCerrar.pack()

    def cargar_datos(self, xRegistros):
        """Carga las filas en la tabla.

        Cada registro debe ser una tupla o lista con este orden:
        (ID Postulante, Fecha Registro, DNI, Area, Puesto, Estado)
        """
        self.tabla.delete(*self.tabla.get_children())
        for xFila in xRegistros:
            self.tabla.insert("", tk.END, values=xFila)