import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from datetime import datetime
import os # Necesario para eliminar la DB en el ejemplo de demostración (opcional)

# Importaciones de estilo (asumo que siguen existiendo, aunque no me pasaste el archivo 'estilos.py')
# from estilos import BG_MODULO, FG_PRIMARY, COLOR_ACCENT, FONT_BASE, FONT_BUTTON, add_logo_header

# --- CONSTANTES DE ESTILO (Simuladas si 'estilos.py' no existe) ---
BG_MODULO = "#1E1E1E"
FG_PRIMARY = "#FFFFFF"
COLOR_ACCENT = "#5E93E4"
FONT_BASE = ('Arial', 10)
FONT_BUTTON = ('Arial', 10, 'bold')

def add_logo_header(frame, title):
    """Función de cabecera simulada."""
    header = ttk.Label(frame, text=title, font=('Arial', 16, 'bold'), 
                       foreground=COLOR_ACCENT, background=BG_MODULO)
    header.pack(pady=10)
# -------------------------------------------------------------------


# Nombre del archivo de la base de datos
DB_NAME = 'produccion.db' 

# === Manejo Global de la Conexión y Base de Datos ===

conexion = None 

try:
    # Intenta establecer la conexión con la DB (Usando 'produccion.db')
    conexion = sqlite3.connect(DB_NAME)
    # Configurar para obtener filas como diccionarios/objetos
    conexion.row_factory = sqlite3.Row 
    print(f"Conexión a SQLite '{DB_NAME}' establecida con éxito.")
except sqlite3.Error as e:
    print(f"Error al conectar a SQLite: {e}")
    # Si la conexión falla, la aplicación no debería continuar
    

def iniciar_db(conn):
    """Crea las tablas Producto, Lote y Control de Calidad si no existen."""
    cursor = conn.cursor()
    
    # 1. Tabla de Productos (Modelado: SKU es clave única)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        sku TEXT NOT NULL UNIQUE
    );
    """)

    # 2. Tabla de Lotes (Modelado: FK a Productos)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Lotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_sku TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        fecha_creacion TEXT NOT NULL,
        FOREIGN KEY (producto_sku) REFERENCES Productos (sku)
    );
    """)
    
    # 3. Tabla de Controles de Calidad (Modelado: FK a Lotes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ControlesCalidad (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lote_id INTEGER NOT NULL,
        parametro TEXT NOT NULL,
        valor REAL NOT NULL,
        aprobado INTEGER NOT NULL, -- 0=Falso, 1=Verdadero
        timestamp TEXT NOT NULL,
        FOREIGN KEY (lote_id) REFERENCES Lotes (id)
    );
    """)
    conn.commit()
    print("Tablas 'Productos', 'Lotes' y 'ControlesCalidad' verificadas/creadas.")

# Aseguramos la inicialización de las tablas al iniciar la conexión
if conexion:
    iniciar_db(conexion)

# ======================================================


class ProduccionUI:
    def __init__(self, root, volver_callback):
        # Configuración de estilos para el frame principal (similar a tu código original)
        style = ttk.Style()
        style.configure("Modulo.TFrame", background=BG_MODULO)
        style.configure("Modulo.TLabel", background=BG_MODULO, foreground=FG_PRIMARY, font=FONT_BASE)
        style.configure("Modulo.TButton", background=COLOR_ACCENT, foreground="black", font=FONT_BUTTON)
        # Configurar TEntry y TNotebook
        style.configure("TEntry", fieldbackground="white", foreground="black", font=FONT_BASE)
        style.map("Modulo.TButton", background=[('active', COLOR_ACCENT)])

        self.frame = ttk.Frame(root, style="Modulo.TFrame") 
        self.frame.pack(fill="both", expand=True) 

        self.volver_callback = volver_callback
        self.crear_ui()
        
        # Cargar datos iniciales
        self.cargar_productos_en_tabla()
        self.cargar_lotes_en_tabla()

    def crear_ui(self):
        """Crea la interfaz de usuario con pestañas para Productos y Lotes/Calidad."""
        
        add_logo_header(self.frame, "Gestión de Producción y Trazabilidad")

        # Usamos un Notebook (Pestañas) para separar las interfaces
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(pady=10, padx=20, fill="both", expand=True)

        # ---------------------------
        # PESTAÑA 1: GESTIÓN DE PRODUCTOS
        # ---------------------------
        self.frame_productos = ttk.Frame(self.notebook, style="Modulo.TFrame")
        self.notebook.add(self.frame_productos, text=" Catálogo de Productos ")
        self.crear_ui_productos(self.frame_productos)

        # ---------------------------
        # PESTAÑA 2: GESTIÓN DE LOTES Y CALIDAD
        # ---------------------------
        self.frame_lotes = ttk.Frame(self.notebook, style="Modulo.TFrame")
        self.notebook.add(self.frame_lotes, text=" Lotes y Calidad ")
        self.crear_ui_lotes(self.frame_lotes)

        # Botón para volver (IMPORTANTE: Usa self.volver_callback)
        ttk.Button(self.frame, text="< Volver al Menú Principal", command=self.volver_callback, style="Modulo.TButton").pack(pady=20, ipadx=10)
    
    # -------------------------------------------------------------
    # ⬇️ INTERFAZ Y LÓGICA DE PRODUCTOS ⬇️
    # -------------------------------------------------------------

    def crear_ui_productos(self, parent_frame):
        """Crea los controles y la tabla para la gestión de productos."""
        
        input_frame = ttk.Frame(parent_frame, style="Modulo.TFrame", padding="15") 
        input_frame.pack(pady=15)
        
        ttk.Label(input_frame, text="Nombre Producto:", style="Modulo.TLabel").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.prod_nombre_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.prod_nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(input_frame, text="SKU (ID Único):", style="Modulo.TLabel").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.prod_sku_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.prod_sku_entry.grid(row=1, column=1, padx=10, pady=5)
        
        button_container = ttk.Frame(parent_frame, style="Modulo.TFrame") 
        button_container.pack(pady=10)
        ttk.Button(button_container, text="Agregar Producto", command=self.agregar_producto, style="Modulo.TButton").pack(side=tk.LEFT, padx=10, ipadx=10)
        ttk.Button(button_container, text="Borrar Seleccionado", command=self.borrar_producto, style="Modulo.TButton").pack(side=tk.LEFT, padx=10, ipadx=10)

        # Tabla de Productos
        columns = ("ID", "Nombre", "SKU")
        table_frame = ttk.Frame(parent_frame, style="Modulo.TFrame") 
        table_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        self.tabla_productos = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tabla_productos.column("ID", width=50, anchor=tk.CENTER)
        for col in columns:
            self.tabla_productos.heading(col, text=col)
            
        self.tabla_productos.pack(side='left', fill="both", expand=True)
        # Scrollbar opcional...

    def agregar_producto(self):
        """Inserta un nuevo producto en la tabla Productos."""
        nombre = self.prod_nombre_entry.get()
        sku = self.prod_sku_entry.get().upper() # Usar mayúsculas para SKU

        if not all([nombre, sku]):
            messagebox.showerror("Error", "El Nombre y el SKU son obligatorios.")
            return

        cursor = conexion.cursor()
        sql_insert = "INSERT INTO Productos (nombre, sku) VALUES (?, ?);"
        
        try:
            cursor.execute(sql_insert, (nombre, sku))
            conexion.commit()
            self.cargar_productos_en_tabla()
            self.prod_nombre_entry.delete(0, tk.END)
            self.prod_sku_entry.delete(0, tk.END)
            messagebox.showinfo("Éxito", f"Producto '{nombre}' (SKU: {sku}) agregado correctamente.")

        except sqlite3.IntegrityError:
            messagebox.showerror("Error de DB", f"Ya existe un producto con el SKU '{sku}'.")
        except sqlite3.Error as e:
            messagebox.showerror("Error de DB", f"Ocurrió un error al insertar: {e}")

    def borrar_producto(self):
        """Elimina el producto seleccionado de la DB."""
        selected_item = self.tabla_productos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona un producto para borrar.")
            return

        item_data = self.tabla_productos.item(selected_item, 'values')
        producto_id = item_data[0] # El ID es el primer valor
        producto_sku = item_data[2] # El SKU es el tercer valor

        if messagebox.askyesno("Confirmar Borrado", f"¿Estás seguro de borrar el producto '{producto_sku}'? (Esto puede afectar lotes asociados)"):
            cursor = conexion.cursor()
            try:
                sql_delete = "DELETE FROM Productos WHERE id = ?;"
                cursor.execute(sql_delete, (producto_id,))
                conexion.commit()
                self.cargar_productos_en_tabla()
                self.cargar_lotes_en_tabla() # Recargar lotes por si se borró un SKU asociado
                messagebox.showinfo("Éxito", f"Producto ID {producto_id} borrado correctamente.")
            except sqlite3.Error as e:
                # Nota: SQLite permite el borrado por defecto, a menos que se use ON DELETE RESTRICT/SET NULL
                messagebox.showerror("Error de DB", f"Ocurrió un error al borrar: {e}")

    def cargar_productos_en_tabla(self):
        """Limpia y rellena la tabla de productos con datos de la DB."""
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
            
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id, nombre, sku FROM Productos ORDER BY nombre ASC")
            productos = cursor.fetchall()
            for prod in productos:
                self.tabla_productos.insert('', 'end', values=tuple(prod))
        except sqlite3.Error as e:
            messagebox.showerror("Error de DB", f"No se pudo cargar la tabla de productos: {e}")

    # -------------------------------------------------------------
    # ⬇️ INTERFAZ Y LÓGICA DE LOTES Y CALIDAD ⬇️
    # -------------------------------------------------------------

    def crear_ui_lotes(self, parent_frame):
        """Crea los controles y la tabla para la gestión de Lotes y Calidad."""
        
        # Frame de Creación de Lotes
        lote_frame = ttk.Frame(parent_frame, style="Modulo.TFrame", padding="15")
        lote_frame.pack(pady=10, fill="x")

        ttk.Label(lote_frame, text="SKU del Producto:", style="Modulo.TLabel").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.lote_sku_entry = ttk.Entry(lote_frame, width=20, style="TEntry")
        self.lote_sku_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(lote_frame, text="Cantidad:", style="Modulo.TLabel").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.lote_cantidad_entry = ttk.Entry(lote_frame, width=15, style="TEntry")
        self.lote_cantidad_entry.grid(row=0, column=3, padx=10, pady=5)

        ttk.Button(lote_frame, text="Crear Nuevo Lote", command=self.crear_lote, style="Modulo.TButton").grid(row=0, column=4, padx=10, pady=5, ipadx=10)

        # Separador entre lotes y calidad
        ttk.Separator(parent_frame, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # Frame de Control de Calidad
        calidad_frame = ttk.Frame(parent_frame, style="Modulo.TFrame", padding="15")
        calidad_frame.pack(pady=10, fill="x")
        
        ttk.Label(calidad_frame, text="Lote ID (para registrar):", style="Modulo.TLabel").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.calidad_lote_id_entry = ttk.Entry(calidad_frame, width=10, style="TEntry")
        self.calidad_lote_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(calidad_frame, text="Parámetro:", style="Modulo.TLabel").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.calidad_parametro_entry = ttk.Entry(calidad_frame, width=15, style="TEntry")
        self.calidad_parametro_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(calidad_frame, text="Valor:", style="Modulo.TLabel").grid(row=0, column=4, padx=10, pady=5, sticky="e")
        self.calidad_valor_entry = ttk.Entry(calidad_frame, width=10, style="TEntry")
        self.calidad_valor_entry.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Label(calidad_frame, text="Aprobado:", style="Modulo.TLabel").grid(row=0, column=6, padx=10, pady=5, sticky="e")
        self.calidad_aprobado_var = tk.BooleanVar()
        ttk.Checkbutton(calidad_frame, text="Sí/No", variable=self.calidad_aprobado_var, 
                        style="Modulo.TCheckbutton").grid(row=0, column=7, padx=5, pady=5)
        
        ttk.Button(calidad_frame, text="Registrar Calidad", command=self.registrar_medicion_calidad, style="Modulo.TButton").grid(row=0, column=8, padx=10, pady=5, ipadx=10)

        # Tabla de Lotes (para mostrar trazabilidad y estatus)
        columns = ("ID Lote", "SKU", "Producto", "Cantidad", "Fecha Creación")
        table_frame = ttk.Frame(parent_frame, style="Modulo.TFrame") 
        table_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        self.tabla_lotes = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tabla_lotes.column("ID Lote", width=80, anchor=tk.CENTER)
        self.tabla_lotes.column("SKU", width=100, anchor=tk.CENTER)
        for col in columns:
            self.tabla_lotes.heading(col, text=col)
            
        self.tabla_lotes.pack(side='left', fill="both", expand=True)
        self.tabla_lotes.bind('<<TreeviewSelect>>', self.mostrar_controles_calidad)

        # Área de Trazabilidad/Calidad Detallada
        self.calidad_detalle_label = ttk.Label(parent_frame, text="Selecciona un Lote para ver los Controles de Calidad...", 
                                               style="Modulo.TLabel", justify=tk.LEFT, wraplength=800)
        self.calidad_detalle_label.pack(pady=10, padx=20, fill="x")

    def crear_lote(self):
        """Inserta un nuevo lote."""
        sku = self.lote_sku_entry.get().upper()
        cantidad_str = self.lote_cantidad_entry.get()

        if not all([sku, cantidad_str]):
            messagebox.showerror("Error", "SKU y Cantidad son obligatorios para crear un lote.")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        cursor = conexion.cursor()
        
        # 1. Verificar si el SKU existe
        cursor.execute("SELECT nombre FROM Productos WHERE sku = ?", (sku,))
        producto = cursor.fetchone()
        if not producto:
            messagebox.showerror("Error", f"El SKU '{sku}' no existe en el catálogo de productos.")
            return

        # 2. Insertar Lote
        fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql_insert = "INSERT INTO Lotes (producto_sku, cantidad, fecha_creacion) VALUES (?, ?, ?);"
        
        try:
            cursor.execute(sql_insert, (sku, cantidad, fecha_creacion))
            conexion.commit()
            self.cargar_lotes_en_tabla()
            self.lote_sku_entry.delete(0, tk.END)
            self.lote_cantidad_entry.delete(0, tk.END)
            messagebox.showinfo("Éxito", f"Lote creado para {producto['nombre']} ({sku}) con {cantidad} unidades.")
        except sqlite3.Error as e:
            messagebox.showerror("Error de DB", f"Ocurrió un error al crear el lote: {e}")

    def registrar_medicion_calidad(self):
        """Registra una medición de calidad para un lote específico."""
        lote_id_str = self.calidad_lote_id_entry.get()
        parametro = self.calidad_parametro_entry.get()
        valor_str = self.calidad_valor_entry.get()
        aprobado = self.calidad_aprobado_var.get()

        if not all([lote_id_str, parametro, valor_str]):
            messagebox.showerror("Error", "Debes completar Lote ID, Parámetro y Valor.")
            return
            
        try:
            lote_id = int(lote_id_str)
            valor = float(valor_str)
        except ValueError:
            messagebox.showerror("Error", "Lote ID debe ser un entero y Valor debe ser un número.")
            return

        cursor = conexion.cursor()
        
        # 1. Verificar si el Lote existe
        cursor.execute("SELECT 1 FROM Lotes WHERE id = ?", (lote_id,))
        if cursor.fetchone() is None:
            messagebox.showerror("Error", f"El Lote ID {lote_id} no existe.")
            return

        # 2. Insertar Control de Calidad
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        aprobado_int = 1 if aprobado else 0
        sql_insert = "INSERT INTO ControlesCalidad (lote_id, parametro, valor, aprobado, timestamp) VALUES (?, ?, ?, ?, ?);"
        
        try:
            cursor.execute(sql_insert, (lote_id, parametro, valor, aprobado_int, timestamp))
            conexion.commit()
            
            # Limpiar campos de calidad
            self.calidad_lote_id_entry.delete(0, tk.END)
            self.calidad_parametro_entry.delete(0, tk.END)
            self.calidad_valor_entry.delete(0, tk.END)
            self.calidad_aprobado_var.set(False)

            messagebox.showinfo("Éxito", f"Medición '{parametro}' registrada para Lote ID {lote_id}.")
            
            # Actualizar detalle si el lote sigue seleccionado (opcional)
            self.mostrar_controles_calidad(None) 
            
        except sqlite3.Error as e:
            messagebox.showerror("Error de DB", f"Ocurrió un error al registrar la calidad: {e}")

    def cargar_lotes_en_tabla(self):
        """Limpia y rellena la tabla de lotes con datos de la DB, incluyendo el nombre del producto."""
        for item in self.tabla_lotes.get_children():
            self.tabla_lotes.delete(item)
            
        cursor = conexion.cursor()
        try:
            # Consulta JOIN para obtener el nombre del producto junto con los datos del lote
            sql_select = """
            SELECT 
                L.id, L.producto_sku, P.nombre, L.cantidad, L.fecha_creacion
            FROM Lotes L
            JOIN Productos P ON L.producto_sku = P.sku
            ORDER BY L.fecha_creacion DESC;
            """
            cursor.execute(sql_select)
            lotes = cursor.fetchall()
            for lote in lotes:
                self.tabla_lotes.insert('', 'end', values=tuple(lote))
        except sqlite3.Error as e:
            messagebox.showerror("Error de DB", f"No se pudo cargar la tabla de lotes: {e}")

    def mostrar_controles_calidad(self, event):
        """Muestra los controles de calidad para el lote seleccionado (Trazabilidad)."""
        selected_item = self.tabla_lotes.selection()
        if not selected_item:
            self.calidad_detalle_label.config(text="Selecciona un Lote para ver los Controles de Calidad...")
            return

        item_data = self.tabla_lotes.item(selected_item, 'values')
        lote_id = item_data[0]
        producto_nombre = item_data[2]
        
        cursor = conexion.cursor()
        sql_select = "SELECT timestamp, parametro, valor, aprobado FROM ControlesCalidad WHERE lote_id = ? ORDER BY timestamp DESC"
        
        try:
            cursor.execute(sql_select, (lote_id,))
            controles = cursor.fetchall()
            
            detalle_text = [f"Controles de Calidad para Lote ID: {lote_id} ({producto_nombre}):\n"]
            
            if not controles:
                detalle_text.append("   - No hay mediciones de calidad registradas para este lote.")
            else:
                for control in controles:
                    aprobado = "✅ APROBADO" if control['aprobado'] == 1 else "❌ RECHAZADO"
                    line = f"   - [{control['timestamp']}] {control['parametro']}: {control['valor']} ({aprobado})"
                    detalle_text.append(line)
                    
            self.calidad_detalle_label.config(text="\n".join(detalle_text))

        except sqlite3.Error as e:
            self.calidad_detalle_label.config(text=f"Error al cargar controles de calidad: {e}")

# -------------------------------------------------------------
# ⬇️ EJEMPLO DE USO (Sustitución del bloque principal) ⬇️
# -------------------------------------------------------------

# Aquí debería ir tu código de inicialización de la aplicación principal
if __name__ == '__main__':
    # Opcional: Borrar el archivo DB para iniciar desde cero en cada ejecución de prueba
    # if os.path.exists(DB_NAME):
    #     os.remove(DB_NAME)

    if conexion:
        root = tk.Tk()
        root.title("Módulo de Producción")
        root.config(bg=BG_MODULO)
        
        # Función dummy para volver (simula el menú principal)
        def volver_al_menu():
            root.quit()

        ProduccionUI(root, volver_al_menu)
        root.mainloop()