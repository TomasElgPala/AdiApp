import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import save_data, load_data

# Se han añadido 'sucursal', 'contacto_mail', 'celular' y 'fecha_de_baja'
DATA_FILE = "empleados.csv"
FIELDNAMES = ["id", "nombre", "puesto", "fecha_ingreso", "sueldo", "sucursal", "contacto_mail", "celular", "fecha_de_baja"]

class EmpleadosUI:
    def __init__(self, frame, volver_callback):
        self.frame = frame
        self.volver_callback = volver_callback
        self.empleados_data = load_data(DATA_FILE)
        self.next_id = self._get_next_id()
        self.crear_ui()
        self.cargar_datos_en_tabla()

    def _get_next_id(self):
        """Genera el siguiente ID único para un nuevo empleado."""
        if not self.empleados_data:
            return 1
        return max(int(e["id"]) for e in self.empleados_data) + 1

    def crear_ui(self):
        """Crea y organiza la interfaz de usuario para la gestión de empleados."""
        # Título
        tk.Label(self.frame, text="Gestión de Empleados", font=("Arial", 18, "bold")).pack(pady=10)

        # Contenedor para los campos de entrada
        input_frame = tk.Frame(self.frame)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Nombre:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.nombre_entry = tk.Entry(input_frame)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Puesto:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.puesto_entry = tk.Entry(input_frame)
        self.puesto_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Fecha Ingreso:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=2, sticky="e")
        self.fecha_ingreso_entry = tk.Entry(input_frame)
        self.fecha_ingreso_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Sueldo:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=2, sticky="e")
        self.sueldo_entry = tk.Entry(input_frame)
        self.sueldo_entry.grid(row=3, column=1, padx=5, pady=2)
        
        # Nuevos campos
        tk.Label(input_frame, text="Sucursal:", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=2, sticky="e")
        self.sucursal_entry = tk.Entry(input_frame)
        self.sucursal_entry.grid(row=4, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Email:", font=("Arial", 12)).grid(row=5, column=0, padx=5, pady=2, sticky="e")
        self.contacto_mail_entry = tk.Entry(input_frame)
        self.contacto_mail_entry.grid(row=5, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Celular:", font=("Arial", 12)).grid(row=6, column=0, padx=5, pady=2, sticky="e")
        self.celular_entry = tk.Entry(input_frame)
        self.celular_entry.grid(row=6, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Fecha de Baja:", font=("Arial", 12)).grid(row=7, column=0, padx=5, pady=2, sticky="e")
        self.fecha_de_baja_entry = tk.Entry(input_frame)
        self.fecha_de_baja_entry.grid(row=7, column=1, padx=5, pady=2)


        # Botón para agregar empleado
        tk.Button(self.frame, text="Agregar Empleado", command=self.agregar_empleado).pack(pady=5)

        # Tabla (Treeview) para mostrar los empleados, se agregaron columnas
        columns = ("ID", "Nombre", "Puesto", "Fecha Ingreso", "Sueldo", "Sucursal", "Email", "Celular", "Fecha de Baja")
        self.tabla = ttk.Treeview(self.frame, columns=columns, show="headings")
        for col in columns:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor=tk.CENTER)
        self.tabla.pack(pady=10, fill="both", expand=True)

        # Botón para borrar empleado
        tk.Button(self.frame, text="Borrar Empleado Seleccionado", command=self.borrar_empleado).pack(pady=5)

        # Botón para volver
        tk.Button(self.frame, text="Volver al Menú Principal", command=self.volver_callback).pack(pady=20)
    
    def agregar_empleado(self):
        """Función para agregar un nuevo empleado a los datos y a la tabla."""
        nombre = self.nombre_entry.get()
        puesto = self.puesto_entry.get()
        fecha_ingreso = self.fecha_ingreso_entry.get()
        sueldo = self.sueldo_entry.get()
        sucursal = self.sucursal_entry.get()
        contacto_mail = self.contacto_mail_entry.get()
        celular = self.celular_entry.get()
        fecha_de_baja = self.fecha_de_baja_entry.get()

        if not all([nombre, puesto, fecha_ingreso, sueldo, sucursal, contacto_mail, celular, fecha_de_baja]):
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        nuevo_empleado = {
            "id": self.next_id,
            "nombre": nombre,
            "puesto": puesto,
            "fecha_ingreso": fecha_ingreso,
            "sueldo": sueldo,
            "sucursal": sucursal,
            "contacto_mail": contacto_mail,
            "celular": celular,
            "fecha_de_baja": fecha_de_baja
        }
        self.empleados_data.append(nuevo_empleado)
        save_data(DATA_FILE, self.empleados_data, FIELDNAMES)
        self.tabla.insert("", "end", values=(self.next_id, nombre, puesto, fecha_ingreso, sueldo, sucursal, contacto_mail, celular, fecha_de_baja))
        self.next_id += 1
        self.limpiar_campos()
        messagebox.showinfo("Empleado Agregado", "El empleado se ha guardado correctamente.")

    def borrar_empleado(self):
        """Función para borrar el empleado seleccionado de los datos y la tabla."""
        selected_item = self.tabla.selection()
        if not selected_item:
            messagebox.showwarning("Ninguna selección", "Por favor, selecciona un empleado para borrar.")
            return

        respuesta = messagebox.askyesno("Confirmar borrado", "¿Estás seguro de que quieres borrar el empleado seleccionado?")
        if respuesta:
            item_id = self.tabla.item(selected_item, "values")[0]
            self.empleados_data = [e for e in self.empleados_data if str(e["id"]) != str(item_id)]
            save_data(DATA_FILE, self.empleados_data, FIELDNAMES)
            self.tabla.delete(selected_item)
            messagebox.showinfo("Borrado exitoso", "El empleado ha sido eliminado.")

    def cargar_datos_en_tabla(self):
        """Carga los datos existentes en el Treeview."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for empleado in self.empleados_data:
            self.tabla.insert("", "end", values=(
                empleado.get("id"),
                empleado.get("nombre"),
                empleado.get("puesto"),
                empleado.get("fecha_ingreso"),
                empleado.get("sueldo"),
                empleado.get("sucursal"),
                empleado.get("contacto_mail"),
                empleado.get("celular"),
                empleado.get("fecha_de_baja")
            ))

    def limpiar_campos(self):
        """Limpia los campos de entrada después de agregar un empleado."""
        self.nombre_entry.delete(0, tk.END)
        self.puesto_entry.delete(0, tk.END)
        self.fecha_ingreso_entry.delete(0, tk.END)
        self.sueldo_entry.delete(0, tk.END)
        self.sucursal_entry.delete(0, tk.END)
        self.contacto_mail_entry.delete(0, tk.END)
        self.celular_entry.delete(0, tk.END)
        self.fecha_de_baja_entry.delete(0, tk.END)
