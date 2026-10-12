import tkinter as tk
from tkinter import ttk

class ListarRequerimientosView:

    def __init__(self, xParent, xRegistros=None):
        self.ventana = tk.Toplevel(xParent)
        self.ventana.title("Listar | Listar Requerimientos")
        self.ventana.grab_set()

        # --- CENTRAR LA VENTANA ---
        xAnchoVentana = 750
        xAltoVentana = 440
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
            text="Lista de Requerimientos",
            font=("Arial", 16, "bold"),
            anchor="center",
        )
        xTitulo.pack(pady=(10, 20))

        # --- TABLA ---
        xColumnas = (
            "ID Proceso",
            "Fecha Proceso",
            "Fecha Ingreso",
            "Fecha Fin Contrato",
            "N° Requeridos",
            "N° Postulantes",
            "Estado",
        )
        xAnchos = (80, 95, 95, 125, 95, 100, 80)

        xFrameTabla = tk.Frame(xMainFrame)
        xFrameTabla.pack()
        self.tabla = ttk.Treeview(
            xFrameTabla, columns=xColumnas, show="headings", height=8
        )
        # Barra de desplazamiento para cuando haya muchos registros
        xScroll = ttk.Scrollbar(xFrameTabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=xScroll.set)
        xScroll.pack(side=tk.RIGHT, fill=tk.Y)
        for xCol, xAncho in zip(xColumnas, xAnchos):
            self.tabla.heading(xCol, text=xCol)
            self.tabla.column(xCol, width=xAncho, anchor="center")
        self.tabla.pack(side=tk.LEFT)

        # --- BOTÓN (Cerrar centrado) ---
        xFrameBotones = tk.Frame(xMainFrame)
        xFrameBotones.pack(pady=20)

        xBtnCerrar = tk.Button(
            xFrameBotones, text="Cerrar", width=12, command=self.ventana.destroy
        )
        xBtnCerrar.pack()

    def cargar_datos(self, xRegistros):
        """Carga las filas en la tabla.

        Cada registro debe ser una tupla o lista con este orden:
        (ID Proceso, Fecha Proceso, Fecha Ingreso, Fecha Fin Contrato,
         N° Requeridos, N° Postulantes, Estado)
        """
        self.tabla.delete(*self.tabla.get_children())
        for xFila in xRegistros:
            self.tabla.insert("", tk.END, values=xFila)
        if not xRegistros:
            # Mostramos un aviso dentro de la tabla cuando no hay datos
            xVacio = ["Sin registros"] + [""] * (len(self.tabla["columns"]) - 1)
            self.tabla.insert("", tk.END, values=xVacio)