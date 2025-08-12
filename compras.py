import tkinter as tk
from tkinter import ttk

def crear_ui(frame, volver_callback):
    tk.Label(frame, text="Gestión de Compras", font=("Arial", 18)).pack(pady=10)

    tk.Label(frame, text="Fecha").pack()
    tk.Entry(frame).pack()

    tk.Label(frame, text="Proveedor").pack()
    tk.Entry(frame).pack()

    tk.Label(frame, text="Monto").pack()
    tk.Entry(frame).pack()

    tk.Button(frame, text="Agregar compra", command=lambda: print("Agregar compra")).pack(pady=5)

    tabla = ttk.Treeview(frame, columns=("ID", "Fecha", "Proveedor", "Monto"), show="headings")
    for col in ("ID", "Fecha", "Proveedor", "Monto"):
        tabla.heading(col, text=col)
    tabla.pack()

    tk.Button(frame, text="Borrar compra", command=lambda: print("Borrar compra")).pack(pady=5)

    # Botón para volver al menú
    tk.Button(frame, text="Volver al Menú", command=volver_callback).pack(pady=20)