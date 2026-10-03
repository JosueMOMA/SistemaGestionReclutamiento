# Vista/menu_principal_view.py
import tkinter as tk
from tkinter import messagebox
# Importamos la nueva vista que acabamos de crear
from Vista.nuevo_requerimiento_view import NuevoRequerimientoView
from Vista.consultar_requerimiento_view import ConsultarRequerimientoView
from Vista.nuevo_postulante_view import NuevoPostulanteView
from Vista.consultar_postulante_view import ConsultarPostulanteView

class MenuPrincipalView:

  def __init__(self, root):
    self.ventana = root
    self.ventana.title("Sistema de Gestión de Reclutamiento")

    # Centrar la ventana principal
    ancho_ventana = 580
    alto_ventana = 300
    ancho_pantalla = self.ventana.winfo_screenwidth()
    alto_pantalla = self.ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    self.crear_menu()

  def mostrar_mensaje(self, opcion):
    messagebox.showinfo("Mensaje", f"Hiciste clic en: {opcion}")

  def abrir_nuevo_requerimiento(self):
    # Llamamos a nuestra vista hija pasándole la ventana principal
    NuevoRequerimientoView(self.ventana)
  def abrir_consultar_requerimiento(self):
    # Llamamos a nuestra vista hija pasándole la ventana principal
    ConsultarRequerimientoView(self.ventana)
  def abrir_nuevo_postulante(self):
    NuevoPostulanteView(self.ventana)
  def abrir_consultar_postulante(self):
    ConsultarPostulanteView(self.ventana)
  def crear_menu(self):
    barra_menu = tk.Menu(self.ventana)

    # --- MENÚ REQUERIMIENTO ---
    menu_requerimiento = tk.Menu(barra_menu, tearoff=0)
    # MODIFICADO: Conectado a la función que abre la ventana del formulario
    menu_requerimiento.add_command(
        label="Nuevo requerimiento", command=self.abrir_nuevo_requerimiento
    )
    menu_requerimiento.add_command(
        label="Consultar requerimiento",
        command=self.abrir_consultar_requerimiento
    )
    barra_menu.add_cascade(label="Requerimiento", menu=menu_requerimiento)

    # --- MENÚ POSTULANTE ---
    menu_postulante = tk.Menu(barra_menu, tearoff=0)
    menu_postulante.add_command(
        label="Nuevo postulante",
        command=self.abrir_nuevo_postulante
    )
    menu_postulante.add_command(
        label="Consultar postulante",
        command=self.abrir_consultar_postulante
    )
    barra_menu.add_cascade(label="Postulante", menu=menu_postulante)

    # --- MENÚ LISTAR ---
    menu_listar = tk.Menu(barra_menu, tearoff=0)
    menu_listar.add_command(
        label="Listar requerimientos",
        command=lambda: self.mostrar_mensaje("Listar requerimientos"),
    )
    menu_listar.add_command(
        label="Listar postulantes",
        command=lambda: self.mostrar_mensaje("Listar postulantes"),
    )
    barra_menu.add_cascade(label="Listar", menu=menu_listar)

    # --- MENÚ ACERCA DE ---
    menu_acerca = tk.Menu(barra_menu, tearoff=0)
    menu_acerca.add_command(
        label="Información del sistema",
        command=lambda: self.mostrar_mensaje("Información del sistema"),
    )
    menu_acerca.add_separator()
    menu_acerca.add_command(label="Salir", command=self.ventana.quit)
    barra_menu.add_cascade(label="Acerca de", menu=menu_acerca)

    self.ventana.config(menu=barra_menu)