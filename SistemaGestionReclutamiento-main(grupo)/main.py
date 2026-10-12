import sys
import traceback
import tkinter as tk
from tkinter import messagebox


def verificar_dependencias():
    # Verificamos que la librería del calendario esté instalada antes de abrir el sistema
    try:
        import tkcalendar  # noqa: F401
        return True
    except ImportError:
        xRaiz = tk.Tk()
        xRaiz.withdraw()
        messagebox.showerror(
            "Falta una librería",
            "No se encontró la librería 'tkcalendar'.\n\n"
            "Instálela con el comando:\n    pip install -r requirements.txt",
        )
        xRaiz.destroy()
        return False


def manejar_error_inesperado(xTipo, xValor, xTraza):
    # Red de seguridad: si ocurre un error no previsto, se muestra un mensaje y el sistema sigue abierto
    traceback.print_exception(xTipo, xValor, xTraza)
    messagebox.showerror(
        "Error inesperado",
        f"Ocurrió un error inesperado y la operación no se completó.\n\nDetalle: {xValor}",
    )


if __name__ == "__main__":
    if not verificar_dependencias():
        sys.exit(1)

    from Modelo.empresa import Empresa
    from Vista.menu_principal_view import MenuPrincipalView

    root = tk.Tk()
    root.report_callback_exception = manejar_error_inesperado

    # Patrón Singleton: esta es la única instancia de Empresa del sistema
    xEmpresaBase = Empresa("20123456789", "Asica Farms")

    app = MenuPrincipalView(root, xEmpresaBase)

    root.mainloop()
