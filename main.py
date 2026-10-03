# main.py
import tkinter as tk
from Vista.menu_principal_view import MenuPrincipalView

if __name__ == "__main__":
  # Creamos la ventana principal de Tkinter
  root = tk.Tk()

  # Instanciamos nuestra vista del menú principal pasándole la ventana raíz
  app = MenuPrincipalView(root)

  # Iniciamos el bucle principal de la aplicación
  root.mainloop()