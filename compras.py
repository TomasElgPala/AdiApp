import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
# from data_manager import save_data, load_data # Ya no se usan
# Importamos BG_MODULO para el fondo negro
from estilos import BG_MODULO, FG_PRIMARY, COLOR_ACCENT, FONT_BASE, FONT_BUTTON, add_logo_header

# DATA_FILE = "compras.csv" # Ya no se usa
# Campo modificado: "sucursal" -> "proveedor"
FIELDNAMES = ["id", "fecha", "proveedor", "monto", "identificador_producto", "cliente"]

# === Manejo Global de la Conexión y Base de Datos ===

# Objeto de conexión global 
conexion = None 

try:
    # Intenta establecer la conexión con la DB
    conexion = sqlite3.connect('adidas.db')
    print(f"Conexión a SQLite ({'adidas.db'}) establecida con éxito.")
except sqlite3.Error as e:
    print(f"Error al conectar a SQLite: {e}")
    messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {e}")


def iniciar_db(conn):
    """Asegura que la tabla 'compras' exista en la base de datos, usando 'proveedor'."""
    cursor = conn.cursor()
    # Campo modificado en la creación de la tabla
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        proveedor TEXT,
        monto REAL NOT NULL,
        identificador_producto TEXT,
        cliente TEXT
    );
    """)
    conn.commit()
    cursor.close()
    print("Tabla 'compras' verificada/creada.")

# Aseguramos la inicialización de la tabla al iniciar la conexión
if conexion:
    iniciar_db(conexion)

# ======================================================


class ComprasUI:
    def __init__(self, root, volver_callback):
        # Crear un frame principal que ocupe todo el root y tenga el fondo negro
        self.frame = ttk.Frame(root, style="Modulo.TFrame") 
        self.frame.pack(fill="both", expand=True) 

        self.volver_callback = volver_callback
        self.crear_ui()
        # Ahora carga los datos directamente desde SQLite
        self.cargar_datos_en_tabla()

    def crear_ui(self, *args, **kwargs):
        """Crea y organiza la interfaz de usuario para la gestión de compras, con estilo negro."""
        
        # 🛠️ Definición de estilos Treeview
        style = ttk.Style(self.frame)
        style.configure("BlackText.Treeview", 
                        font=("Segoe UI", 10),
                        rowheight=25,
                        fieldbackground="white")
                        
        style.configure("BlackText.Treeview.Heading",
                        font=("Segoe UI", 11, "bold"),
                        background=COLOR_ACCENT, 
                        foreground=FG_PRIMARY, 
                        relief="flat")
        
        # Encabezado con el "Logo"
        add_logo_header(self.frame, "Gestión de Compras (Seguimiento de Pedidos)")

        # Contenedor para los campos de entrada (fondo negro)
        input_frame = ttk.Frame(self.frame, style="Modulo.TFrame", padding="15")
        input_frame.pack(pady=15)

        # Fila 0
        ttk.Label(input_frame, text="Fecha (DD/MM/YYYY):", font=FONT_BASE, style="Modulo.TLabel").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.fecha_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.fecha_entry.grid(row=0, column=1, padx=10, pady=5)

        # CAMBIO: "Sucursal" a "Proveedor"
        ttk.Label(input_frame, text="Proveedor:", font=FONT_BASE, style="Modulo.TLabel").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.proveedor_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.proveedor_entry.grid(row=0, column=3, padx=10, pady=5)

        # Fila 1
        ttk.Label(input_frame, text="Monto ($):", font=FONT_BASE, style="Modulo.TLabel").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.monto_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.monto_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Identificador del Producto:", font=FONT_BASE, style="Modulo.TLabel").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.identificador_producto_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.identificador_producto_entry.grid(row=1, column=3, padx=10, pady=5)

        # Fila 2
        ttk.Label(input_frame, text="Cliente:", font=FONT_BASE, style="Modulo.TLabel").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.cliente_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.cliente_entry.grid(row=2, column=1, padx=10, pady=5)

        # Botones de acción (fondo negro)
        button_container = ttk.Frame(self.frame, style="Modulo.TFrame")
        button_container.pack(pady=10)

        # Botones usan estilo Modulo.TButton (Blanco con texto negro)
        ttk.Button(button_container, text="Agregar Compra (Pedido)", command=self.agregar_compra, style="Modulo.TButton").pack(side=tk.LEFT, padx=10, ipadx=10)
        ttk.Button(button_container, text="Borrar Seleccionado", command=self.borrar_compra, style="Modulo.TButton").pack(side=tk.LEFT, padx=10, ipadx=10)


        # Tabla (Treeview) para mostrar las compras
        # CAMBIO: "Sucursal" a "Proveedor"
        columns = ("ID", "Fecha", "Proveedor", "Monto", "Identificador Producto", "Cliente")
        
        table_frame = ttk.Frame(self.frame, style="Modulo.TFrame")
        table_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        self.tabla = ttk.Treeview(table_frame, columns=columns, show="headings", style="BlackText.Treeview")
        
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        vsb.pack(side='right', fill='y')
        self.tabla.configure(yscrollcommand=vsb.set)

        for col in columns:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor=tk.CENTER)
            
        self.tabla.pack(side='left', fill="both", expand=True)

        # Botón para volver (Blanco con texto negro)
        ttk.Button(self.frame, text="< Volver al Menú Principal", command=self.volver_callback, style="Modulo.TButton").pack(pady=20, ipadx=10)
    
    
    # -------------------------------------------------------------
    # ⬇️ FUNCIONES DE GESTIÓN DE DATOS ADAPTADAS A SQLITE ⬇️
    # -------------------------------------------------------------

    def agregar_compra(self):
        """Recoge los datos, valida y agrega una nueva compra a la DB."""
        fecha = self.fecha_entry.get()
        # CAMBIO: Usar self.proveedor_entry
        proveedor = self.proveedor_entry.get() 
        monto_str = self.monto_entry.get()
        identificador_producto = self.identificador_producto_entry.get()
        cliente = self.cliente_entry.get()

        # CAMBIO: Usar proveedor en la validación
        if not all([fecha, proveedor, monto_str, identificador_producto, cliente]):
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")
            return

        try:
            monto = float(monto_str)
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido.")
            return

        cursor = conexion.cursor()
        
        # CAMBIO: Usar columna 'proveedor' y variable 'proveedor'
        sql_insert = """
        INSERT INTO compras (fecha, proveedor, monto, identificador_producto, cliente)
        VALUES (?, ?, ?, ?, ?);
        """
        datos = (fecha, proveedor, monto, identificador_producto, cliente)

        try:
            cursor.execute(sql_insert, datos)
            conexion.commit() # Guardar los cambios en la DB
            
            self.cargar_datos_en_tabla()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Compra agregada correctamente.")

        except sqlite3.Error as e:
             messagebox.showerror("Error de DB", f"Ocurrió un error al insertar: {e}")
        finally:
            cursor.close()


    def borrar_compra(self):
        """Elimina la compra seleccionada de la DB."""
        selected_item = self.tabla.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona una compra para borrar.")
            return

        item_data = self.tabla.item(selected_item, 'values')
        compra_id = item_data[0] # El ID es el primer valor

        if messagebox.askyesno("Confirmar Borrado", f"¿Estás seguro de que deseas borrar la compra ID {compra_id}?"):
            cursor = conexion.cursor()
            
            try:
                # Consulta DELETE (no necesita cambios)
                sql_delete = "DELETE FROM compras WHERE id = ?;"
                cursor.execute(sql_delete, (compra_id,))
                conexion.commit() # Guardar los cambios
                
                # Recargar la tabla
                self.cargar_datos_en_tabla()
                messagebox.showinfo("Éxito", f"Compra ID {compra_id} borrada correctamente.")

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
            # Consulta SELECT (no necesita cambios)
            cursor.execute("SELECT * FROM compras ORDER BY id DESC")
            compras = cursor.fetchall()
            
            # Insertar nuevos datos
            for compra in compras:
                # La tupla compra ya trae los datos en el orden correcto (..., proveedor, monto, ...)
                self.tabla.insert('', 'end', values=compra)

        except sqlite3.Error as e:
             messagebox.showerror("Error de DB", f"No se pudo cargar la tabla: {e}")
        finally:
            cursor.close()
            
    # -------------------------------------------------------------
    # ⬆️ FIN DE FUNCIONES ADAPTADAS ⬆️
    # -------------------------------------------------------------

    def limpiar_campos(self):
        """Limpia los campos de entrada de la UI."""
        self.fecha_entry.delete(0, tk.END)
        # CAMBIO: Limpiar self.proveedor_entry
        self.proveedor_entry.delete(0, tk.END) 
        self.monto_entry.delete(0, tk.END)
        self.identificador_producto_entry.delete(0, tk.END)
        self.cliente_entry.delete(0, tk.END)