import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import save_data, load_data
# Esta línea debe tener TODOS los elementos que usas en el archivo:
from estilos import BG_MODULO, FG_PRIMARY, COLOR_ACCENT, FONT_BASE, FONT_BUTTON, add_logo_header

DATA_FILE = "empleados.csv"
FIELDNAMES = ["id", "nombre", "puesto", "fecha_ingreso", "sueldo", "sucursal", "contacto_mail", "celular", "fecha_de_baja"]

class EmpleadosUI:
    def __init__(self, root, volver_callback):
        # Crear un frame principal que ocupe todo el root y tenga el fondo negro
        self.frame = ttk.Frame(root, style="Modulo.TFrame") 
        self.frame.pack(fill="both", expand=True) 

        self.volver_callback = volver_callback
        self.empleados_data = load_data(DATA_FILE)
        self.next_id = self._get_next_id()
        self.crear_ui()
        self.cargar_datos_en_tabla()

    def _get_next_id(self):
        """Calcula el siguiente ID disponible."""
        if not self.empleados_data:
            return 1
        return max(int(e["id"]) for e in self.empleados_data) + 1

    def crear_ui(self):
        """Crea y organiza la interfaz de usuario para la gestión de empleados, con estilo negro."""
        
        # Encabezado (usará COLOR_ACCENT)
        add_logo_header(self.frame, "Gestión de Empleados")

        # Contenedor para los campos de entrada (fondo negro)
        input_frame = ttk.Frame(self.frame, style="Modulo.TFrame", padding="15") 
        input_frame.pack(pady=15)
        
        # Fila 0
        ttk.Label(input_frame, text="Nombre:", font=FONT_BASE, style="Modulo.TLabel").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.nombre_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(input_frame, text="Puesto:", font=FONT_BASE, style="Modulo.TLabel").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.puesto_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.puesto_entry.grid(row=0, column=3, padx=10, pady=5)
        
        # Fila 1
        ttk.Label(input_frame, text="Fecha Ingreso (DD/MM/YYYY):", font=FONT_BASE, style="Modulo.TLabel").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.fecha_ingreso_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.fecha_ingreso_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(input_frame, text="Sueldo:", font=FONT_BASE, style="Modulo.TLabel").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.sueldo_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.sueldo_entry.grid(row=1, column=3, padx=10, pady=5)
        
        # Fila 2
        ttk.Label(input_frame, text="Sucursal:", font=FONT_BASE, style="Modulo.TLabel").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.sucursal_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.sucursal_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(input_frame, text="Email:", font=FONT_BASE, style="Modulo.TLabel").grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.contacto_mail_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.contacto_mail_entry.grid(row=2, column=3, padx=10, pady=5)

        # Fila 3
        ttk.Label(input_frame, text="Celular:", font=FONT_BASE, style="Modulo.TLabel").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.celular_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.celular_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Fecha de Baja (Opcional):", font=FONT_BASE, style="Modulo.TLabel").grid(row=3, column=2, padx=10, pady=5, sticky="e")
        self.fecha_de_baja_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.fecha_de_baja_entry.grid(row=3, column=3, padx=10, pady=5)

        # Botones de acción (fondo negro)
        button_container = ttk.Frame(self.frame, style="Modulo.TFrame") 
        button_container.pack(pady=10)

        # Botones usan estilo Modulo.TButton (Blanco con texto negro)
        ttk.Button(button_container, text="Agregar Empleado", command=self.agregar_empleado, style="Modulo.TButton").pack(side=tk.LEFT, padx=10, ipadx=10)
        ttk.Button(button_container, text="Borrar Seleccionado", command=self.borrar_empleado, style="Modulo.TButton").pack(side=tk.LEFT, padx=10, ipadx=10)
        
        # Tabla (Treeview)
        columns = ("ID", "Nombre", "Puesto", "Fecha Ingreso", "Sueldo", "Sucursal", "Email", "Celular", "Fecha de Baja")
        
        table_frame = ttk.Frame(self.frame, style="Modulo.TFrame") 
        table_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        self.tabla = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        vsb.pack(side='right', fill='y')
        self.tabla.configure(yscrollcommand=vsb.set)
        
        for col in columns:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor=tk.CENTER)
            
        self.tabla.pack(side='left', fill="both", expand=True)

        # Botón para volver (IMPORTANTE: Usa self.volver_callback para volver al menú principal)
        ttk.Button(self.frame, text="< Volver al Menú Principal", command=self.volver_callback, style="Modulo.TButton").pack(pady=20, ipadx=10)
    
    def agregar_empleado(self):
        """Recoge los datos, valida y agrega un nuevo empleado."""
        nombre = self.nombre_entry.get()
        puesto = self.puesto_entry.get()
        fecha_ingreso = self.fecha_ingreso_entry.get()
        sueldo = self.sueldo_entry.get()
        sucursal = self.sucursal_entry.get()
        contacto_mail = self.contacto_mail_entry.get()
        celular = self.celular_entry.get()
        fecha_de_baja = self.fecha_de_baja_entry.get() or "" # Puede ser vacío

        if not all([nombre, puesto, fecha_ingreso, sueldo, sucursal, contacto_mail, celular]):
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")
            return

        try:
            float(sueldo)
        except ValueError:
            messagebox.showerror("Error", "El sueldo debe ser un número válido.")
            return

        nuevo_empleado = {
            "id": str(self.next_id),
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
        self.cargar_datos_en_tabla()
        self.limpiar_campos()
        self.next_id = self._get_next_id() # Actualiza el ID
        messagebox.showinfo("Éxito", f"Empleado {nombre} agregado con ID {nuevo_empleado['id']}.")

    def borrar_empleado(self):
        """Elimina el empleado seleccionado de la tabla y los datos."""
        selected_item = self.tabla.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona un empleado para borrar.")
            return

        item_data = self.tabla.item(selected_item, 'values')
        empleado_id = item_data[0] # El ID es el primer valor

        if messagebox.askyesno("Confirmar Borrado", f"¿Estás seguro de que deseas borrar el empleado ID {empleado_id}?"):
            # Filtrar la lista de datos para excluir el empleado
            self.empleados_data = [e for e in self.empleados_data if e.get("id") != empleado_id]
            
            # Guardar los datos actualizados
            save_data(DATA_FILE, self.empleados_data, FIELDNAMES)
            
            # Recargar la tabla
            self.cargar_datos_en_tabla()
            messagebox.showinfo("Éxito", f"Empleado ID {empleado_id} borrado correctamente.")
            self.next_id = self._get_next_id() # Recalcula el siguiente ID

    def cargar_datos_en_tabla(self):
        """Limpia la tabla y la rellena con los datos actuales."""
        # Limpiar la tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        # Insertar nuevos datos
        for empleado in self.empleados_data:
            self.tabla.insert('', 'end', values=(
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
        """Limpia los campos de entrada de la UI."""
        self.nombre_entry.delete(0, tk.END)
        self.puesto_entry.delete(0, tk.END)
        self.fecha_ingreso_entry.delete(0, tk.END)
        self.sueldo_entry.delete(0, tk.END)
        self.sucursal_entry.delete(0, tk.END)
        self.contacto_mail_entry.delete(0, tk.END)
        self.celular_entry.delete(0, tk.END)
        self.fecha_de_baja_entry.delete(0, tk.END)