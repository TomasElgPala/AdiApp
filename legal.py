import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
# Importamos los estilos y componentes necesarios
from estilos import BG_MODULO, FG_PRIMARY, COLOR_ACCENT, FONT_BASE, FONT_BUTTON, add_logo_header
import os # Necesario para la simulación de ruta de archivo

# Definición de columnas para la tabla de documentos
FIELDNAMES = ["id", "tipo", "descripcion", "fecha_firma", "fecha_vencimiento", "archivo_ruta"]

# === Manejo Global de la Conexión y Base de Datos ===
# Usamos el mismo archivo de base de datos que empleados.py
conexion = None 

try:
    # Intenta establecer la conexión con la DB
    conexion = sqlite3.connect('adidas.db')
    print("Conexión a SQLite establecida para módulo Legal.")
except sqlite3.Error as e:
    print(f"Error al conectar a SQLite en legal.py: {e}")

def iniciar_db_legal(conn):
    """Asegura que la tabla 'documentos_legales' exista en la base de datos."""
    if not conn:
        print("Error: Conexión a la base de datos no disponible.")
        return
        
    cursor = conn.cursor()
    # Tabla para guardar documentos legales (licencias, contratos, etc.)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documentos_legales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        descripcion TEXT,
        fecha_firma TEXT,
        fecha_vencimiento TEXT,
        archivo_ruta TEXT
    );
    """)
    conn.commit()
    print("Tabla 'documentos_legales' verificada/creada.")

# Aseguramos la inicialización de la tabla al iniciar la conexión
if conexion:
    iniciar_db_legal(conexion)

# ======================================================


class LegalUI:
    """Interfaz de usuario para la gestión de Documentos Legales (Licencias, Contratos)."""
    def __init__(self, root, volver_callback):
        # Crear un frame principal que ocupe todo el root
        self.frame = ttk.Frame(root, style="Modulo.TFrame") 
        self.frame.pack(fill="both", expand=True) 

        self.volver_callback = volver_callback
        self.crear_ui()
        self.cargar_documentos_en_tabla()

    def crear_ui(self):
        """Crea y organiza la interfaz de usuario para la gestión de documentos legales."""
        
        # Encabezado 
        self.header_frame = add_logo_header(self.frame, "Gestión de Documentos Legales y Contratos")
        
        # Contenedor para los campos de entrada (fondo gris claro)
        input_frame = ttk.Frame(self.frame, style="Modulo.TFrame", padding="15") 
        input_frame.pack(pady=15, padx=20, fill='x')
        
        # --- Entradas de Datos ---
        
        # Fila 0: Tipo y Descripción
        ttk.Label(input_frame, text="Tipo (Licencia, Contrato, etc.):", font=FONT_BASE, style="Modulo.TLabel").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.tipo_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.tipo_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(input_frame, text="Descripción:", font=FONT_BASE, style="Modulo.TLabel").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.descripcion_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.descripcion_entry.grid(row=0, column=3, padx=10, pady=5)
        
        # Fila 1: Fechas
        ttk.Label(input_frame, text="Fecha de Firma (DD/MM/YYYY):", font=FONT_BASE, style="Modulo.TLabel").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.fecha_firma_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.fecha_firma_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(input_frame, text="Fecha de Vencimiento (Opcional):", font=FONT_BASE, style="Modulo.TLabel").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.fecha_vencimiento_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.fecha_vencimiento_entry.grid(row=1, column=3, padx=10, pady=5)
        
        # Fila 2: Ruta de Archivo (Simulada)
        ttk.Label(input_frame, text="Ruta de Archivo (Simulada):", font=FONT_BASE, style="Modulo.TLabel").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        # Usamos mayor ancho para la ruta
        self.archivo_ruta_entry = ttk.Entry(input_frame, width=60, style="TEntry") 
        self.archivo_ruta_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="ew")

        # --- Botones de acción ---
        button_container = ttk.Frame(self.frame, style="Modulo.TFrame") 
        button_container.pack(pady=10)

        # Usamos el estilo 'Accent.TButton' para la acción principal
        ttk.Button(button_container, text="➕ Agregar Documento", command=self.agregar_documento, style="Accent.TButton").pack(side=tk.LEFT, padx=10, ipadx=10)
        ttk.Button(button_container, text="🗑️ Borrar Seleccionado", command=self.borrar_documento, style="Standard.TButton").pack(side=tk.LEFT, padx=10, ipadx=10)
        
        # --- Tabla (Treeview) ---
        columns = ("ID", "Tipo", "Descripción", "Firma", "Vencimiento", "Ruta de Archivo")
        
        table_frame = ttk.Frame(self.frame, style="Modulo.TFrame") 
        table_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        self.tabla = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        vsb.pack(side='right', fill='y')
        self.tabla.configure(yscrollcommand=vsb.set)
        
        for col in columns:
            self.tabla.heading(col, text=col)
            # Ajustar anchos
            if col == "Ruta de Archivo":
                self.tabla.column(col, width=200, anchor=tk.W)
            elif col == "Descripción":
                self.tabla.column(col, width=150, anchor=tk.W)
            else:
                self.tabla.column(col, width=100, anchor=tk.CENTER)
            
        self.tabla.pack(side='left', fill="both", expand=True)

        # Botón para volver
        ttk.Button(self.frame, text="< Volver al Menú Principal", command=self.volver_callback, style="Standard.TButton").pack(pady=20, ipadx=10)
    
    
    # -------------------------------------------------------------
    # ⬇️ FUNCIONES DE GESTIÓN DE DATOS (SQLITE) ⬇️
    # -------------------------------------------------------------
    
    def agregar_documento(self):
        """Recoge los datos, valida y agrega un nuevo documento a la DB."""
        if not conexion:
            messagebox.showerror("Error de DB", "No hay conexión a la base de datos.")
            return

        tipo = self.tipo_entry.get()
        descripcion = self.descripcion_entry.get()
        fecha_firma = self.fecha_firma_entry.get()
        fecha_vencimiento = self.fecha_vencimiento_entry.get() or "" 
        archivo_ruta = self.archivo_ruta_entry.get() or "N/A"

        if not all([tipo, descripcion, fecha_firma]):
            messagebox.showerror("Error", "Por favor, completa Tipo, Descripción y Fecha de Firma.")
            return
            
        cursor = conexion.cursor()
        
        # Consulta de inserción con marcadores de posición (?)
        sql_insert = """
        INSERT INTO documentos_legales (tipo, descripcion, fecha_firma, fecha_vencimiento, archivo_ruta)
        VALUES (?, ?, ?, ?, ?);
        """
        datos = (tipo, descripcion, fecha_firma, fecha_vencimiento, archivo_ruta)

        try:
            cursor.execute(sql_insert, datos)
            conexion.commit() # Guardar los cambios en la DB
            
            self.cargar_documentos_en_tabla()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", f"Documento '{tipo}' agregado correctamente.")

        except sqlite3.Error as e:
            messagebox.showerror("Error de DB", f"Ocurrió un error al insertar el documento: {e}")
        finally:
            cursor.close()

    def borrar_documento(self):
        """Elimina el documento seleccionado de la DB."""
        if not conexion:
            messagebox.showerror("Error de DB", "No hay conexión a la base de datos.")
            return

        selected_item = self.tabla.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona un documento para borrar.")
            return

        item_data = self.tabla.item(selected_item, 'values')
        documento_id = item_data[0] # El ID es el primer valor

        if messagebox.askyesno("Confirmar Borrado", f"¿Estás seguro de que deseas borrar el documento ID {documento_id}?"):
            cursor = conexion.cursor()
            
            try:
                # Consulta DELETE
                sql_delete = "DELETE FROM documentos_legales WHERE id = ?;"
                cursor.execute(sql_delete, (documento_id,))
                conexion.commit() # Guardar los cambios
                
                # Recargar la tabla
                self.cargar_documentos_en_tabla()
                messagebox.showinfo("Éxito", f"Documento ID {documento_id} borrado correctamente.")

            except sqlite3.Error as e:
                messagebox.showerror("Error de DB", f"Ocurrió un error al borrar: {e}")
            finally:
                cursor.close()

    def cargar_documentos_en_tabla(self):
        """Limpia la tabla y la rellena con los datos actuales de la DB."""
        if not conexion:
            return
            
        # Limpiar la tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        cursor = conexion.cursor()
        
        try:
            # Consulta SELECT
            cursor.execute("SELECT * FROM documentos_legales ORDER BY id ASC")
            documentos = cursor.fetchall()
            
            # Insertar nuevos datos
            for doc in documentos:
                self.tabla.insert('', 'end', values=doc)

        except sqlite3.Error as e:
            messagebox.showerror("Error de DB", f"No se pudo cargar la tabla de documentos: {e}")
        finally:
            cursor.close()
            
    # -------------------------------------------------------------
    # ⬆️ FIN DE FUNCIONES DE GESTIÓN DE DATOS ⬆️
    # -------------------------------------------------------------

    def limpiar_campos(self):
        """Limpia los campos de entrada de la UI."""
        self.tipo_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.fecha_firma_entry.delete(0, tk.END)
        self.fecha_vencimiento_entry.delete(0, tk.END)
        self.archivo_ruta_entry.delete(0, tk.END)