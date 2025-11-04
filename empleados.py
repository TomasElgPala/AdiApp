import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
# from data_manager import save_data, load_data # Ya no se usan
# Esta línea debe tener TODOS los elementos que usas en el archivo:
from estilos import BG_MODULO, FG_PRIMARY, COLOR_ACCENT, FONT_BASE, FONT_BUTTON, add_logo_header

# DATA_FILE = "empleados.csv" # Ya no se usa
FIELDNAMES = ["id", "nombre", "puesto", "fecha_ingreso", "sueldo", "sucursal", "contacto_mail", "celular", "fecha_de_baja"]

# === Manejo Global de la Conexión y Base de Datos ===

# Objeto de conexión global (se reasignará en el bloque principal)
conexion = None 

try:
    # Intenta establecer la conexión con la DB
    conexion = sqlite3.connect('adidas.db')
    print("Conexión a SQLite establecida con éxito.")
except sqlite3.Error as e:
    print(f"Error al conectar a SQLite: {e}")
    # Si la conexión falla, la aplicación no debería continuar
    

def iniciar_db(conn):
    """Asegura que la tabla 'empleados' exista en la base de datos."""
    cursor = conn.cursor()
    # Usamos REAL para el sueldo y TEXT para todo lo demás, ID es Primary Key autoincremental
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        puesto TEXT,
        fecha_ingreso TEXT,
        sueldo REAL,
        sucursal TEXT,
        contacto_email TEXT,
        celular INTEGER,
        fecha_de_baja TEXT
    );
    """)
    conn.commit()
    print("Tabla 'empleados' verificada/creada.")

# Aseguramos la inicialización de la tabla al iniciar la conexión
if conexion:
    iniciar_db(conexion)

# ======================================================


class EmpleadosUI:
    def __init__(self, root, volver_callback):
        # Crear un frame principal que ocupe todo el root y tenga el fondo negro
        self.frame = ttk.Frame(root, style="Modulo.TFrame") 
        self.frame.pack(fill="both", expand=True) 

        self.volver_callback = volver_callback
        # self.empleados_data = load_data(DATA_FILE) # Ya no se carga de CSV
        # self.next_id = self._get_next_id() # Ya no es necesario

        self.crear_ui()
        # La tabla ahora carga datos directamente de la DB
        self.cargar_datos_en_tabla() 

    # Se elimina la función _get_next_id, SQLite maneja el ID

    def crear_ui(self):
        """Crea y organiza la interfaz de usuario para la gestión de empleados, con estilo negro."""
        
        # ... (El código de la interfaz de usuario Tkinter sigue igual) ...
        
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
    
    
    # -------------------------------------------------------------
    # ⬇️ FUNCIONES DE GESTIÓN DE DATOS ADAPTADAS A SQLITE ⬇️
    # -------------------------------------------------------------
    
    def agregar_empleado(self):
        """Recoge los datos, valida y agrega un nuevo empleado a la DB."""
        nombre = self.nombre_entry.get()
        puesto = self.puesto_entry.get()
        fecha_ingreso = self.fecha_ingreso_entry.get()
        sueldo_str = self.sueldo_entry.get()
        sucursal = self.sucursal_entry.get()
        contacto_mail = self.contacto_mail_entry.get()
        celular = self.celular_entry.get()
        fecha_de_baja = self.fecha_de_baja_entry.get() or "" 

        if not all([nombre, puesto, fecha_ingreso, sueldo_str, sucursal, contacto_mail, celular]):
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")
            return

        try:
            sueldo = float(sueldo_str)
        except ValueError:
            messagebox.showerror("Error", "El sueldo debe ser un número válido.")
            return
            
        cursor = conexion.cursor()
        
        # Consulta de inserción con marcadores de posición (?)
        sql_insert = """
        INSERT INTO empleados (nombre, puesto, fecha_ingreso, sueldo, sucursal, contacto_mail, celular, fecha_de_baja)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        datos = (nombre, puesto, fecha_ingreso, sueldo, sucursal, contacto_mail, celular, fecha_de_baja)

        try:
            cursor.execute(sql_insert, datos)
            conexion.commit() # Guardar los cambios en la DB
            
            self.cargar_datos_en_tabla()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", f"Empleado {nombre} agregado correctamente.")

        except sqlite3.Error as e:
             messagebox.showerror("Error de DB", f"Ocurrió un error al insertar: {e}")
        finally:
            cursor.close()

    def borrar_empleado(self):
        """Elimina el empleado seleccionado de la DB."""
        selected_item = self.tabla.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona un empleado para borrar.")
            return

        item_data = self.tabla.item(selected_item, 'values')
        empleado_id = item_data[0] # El ID es el primer valor

        if messagebox.askyesno("Confirmar Borrado", f"¿Estás seguro de que deseas borrar el empleado ID {empleado_id}?"):
            cursor = conexion.cursor()
            
            try:
                # Consulta DELETE
                sql_delete = "DELETE FROM empleados WHERE id = ?;"
                cursor.execute(sql_delete, (empleado_id,))
                conexion.commit() # Guardar los cambios
                
                # Recargar la tabla
                self.cargar_datos_en_tabla()
                messagebox.showinfo("Éxito", f"Empleado ID {empleado_id} borrado correctamente.")

            except sqlite3.Error as e:
                 messagebox.showerror("Error de DB", f"Ocurrió un error al borrar: {e}")
            finally:
                cursor.close()

    def cargar_datos_en_tabla(self):
        """Limpia la tabla y la rellena con los datos actuales de la DB."""
        # Limpiar la tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        cursor = conexion.cursor()
        
        try:
            # Consulta SELECT
            cursor.execute("SELECT * FROM empleados ORDER BY id ASC")
            empleados = cursor.fetchall()
            
            # Insertar nuevos datos
            for empleado in empleados:
                # Los valores en 'empleado' son tuplas (id, nombre, puesto, ...)
                self.tabla.insert('', 'end', values=empleado)

        except sqlite3.Error as e:
             messagebox.showerror("Error de DB", f"No se pudo cargar la tabla: {e}")
        finally:
            cursor.close()
            
    # -------------------------------------------------------------
    # ⬆️ FIN DE FUNCIONES ADAPTADAS ⬆️
    # -------------------------------------------------------------

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