import tkinter as tk
from Vista.menu_principal_view import MenuPrincipalView
from Modelo.empresa import Empresa

if __name__ == "__main__":
    root = tk.Tk()

    xEmpresaBase = Empresa("20123456789", "Asica Farms")

    app = MenuPrincipalView(root, xEmpresaBase)

    root.mainloop()