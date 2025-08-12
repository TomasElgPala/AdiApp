import tkinter as tk
import empleados
import compras

# ---- Ventana principal ----
ventana = tk.Tk()
ventana.title("AdiApp - Gestión de Adidas")
ventana.geometry("750x550")

# Frame donde se mostrará la pantalla actual
frame_actual = tk.Frame(ventana)
frame_actual.pack(fill="both", expand=True)

# ---- Funciones para cambiar de pantalla ----
def mostrar_menu():
    limpiar_frame()
    tk.Label(frame_actual, text="Menú Principal", font=("Arial", 20)).pack(pady=20)
    tk.Button(frame_actual, text="Empleados", width=20, command=mostrar_empleados).pack(pady=10)
    tk.Button(frame_actual, text="Compras", width=20, command=mostrar_compras).pack(pady=10)
    tk.Button(frame_actual, text="Salir", width=20, command=ventana.quit).pack(pady=10)

def mostrar_empleados():
    limpiar_frame()
    empleados.crear_ui(frame_actual, mostrar_menu)

def mostrar_compras():
    limpiar_frame()
    compras.crear_ui(frame_actual, mostrar_menu)

def limpiar_frame():
    for widget in frame_actual.winfo_children():
        widget.destroy()

# Mostrar menú inicial
mostrar_menu()

ventana.mainloop()