import tkinter as tk
from tkinter import messagebox
from compras import ComprasUI
from empleados import EmpleadosUI

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AdiApp - Gestión de Adidas")
        self.root.geometry("750x550")
        self.current_frame = None
        self.show_main_menu()

    def show_main_menu(self):
        """Muestra el menú principal de la aplicación."""
        self.limpiar_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        tk.Label(self.current_frame, text="Bienvenido a la Gestión de Empresa", font=("Arial", 20, "bold")).pack(pady=40)
        
        button_style = {"font": ("Arial", 14), "padx": 20, "pady": 10, "relief": "raised"}
        
        tk.Button(self.current_frame, text="Gestión de Compras", command=self.show_compras, **button_style).pack(pady=10)
        tk.Button(self.current_frame, text="Gestión de Empleados", command=self.show_empleados, **button_style).pack(pady=10)
        tk.Button(self.current_frame, text="Salir", command=self.root.quit, **button_style).pack(pady=20)

    def show_compras(self):
        """Muestra la interfaz de gestión de compras."""
        self.limpiar_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        ComprasUI(self.current_frame, self.show_main_menu)

    def show_empleados(self):
        """Muestra la interfaz de gestión de empleados."""
        self.limpiar_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        EmpleadosUI(self.current_frame, self.show_main_menu)

    def limpiar_frame(self):
        """Elimina todos los widgets del frame actual."""
        if self.current_frame:
            for widget in self.current_frame.winfo_children():
                widget.destroy()
            self.current_frame.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
