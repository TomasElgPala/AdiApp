import tkinter as tk
from tkinter import ttk

def crear_ui(frame, volver_callback):
    tk.Label(frame, text="Gestión de Empleados", font=("Arial", 18)).pack(pady=10)

    tk.Label(frame, text="Nombre").pack()
    tk.Entry(frame).pack()

    tk.Label(frame, text="Puesto").pack()
    tk.Entry(frame).pack()

    tk.Label(frame, text="Fecha ingreso").pack()
    tk.Entry(frame).pack()

    tk.Label(frame, text="Sueldo").pack()
    tk.Entry(frame).pack()

    tk.Button(frame, text="Agregar empleado", command=lambda: print("Agregar empleado")).pack(pady=5)

    tabla = ttk.Treeview(frame, columns=("ID", "Nombre", "Puesto", "Fecha", "Sueldo"), show="headings")
    for col in ("ID", "Nombre", "Puesto", "Fecha", "Sueldo"):
        tabla.heading(col, text=col)
    tabla.pack()

    tk.Button(frame, text="Borrar empleado", command=lambda: print("Borrar empleado")).pack(pady=5)

    # Botón para volver al menú
    tk.Button(frame, text="Volver al Menú", command=volver_callback).pack(pady=20)