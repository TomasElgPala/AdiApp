import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import save_data, load_data

# Se han cambiado los nombres de los campos a 'sucursal' y 'identificador_producto'
DATA_FILE = "compras.csv"
FIELDNAMES = ["id", "fecha", "sucursal", "monto", "identificador_producto", "cliente"]

class ComprasUI:
    def __init__(self, frame, volver_callback):
        self.frame = frame
        self.volver_callback = volver_callback
        self.compras_data = load_data(DATA_FILE)
        self.next_id = self._get_next_id()
        self.crear_ui()
        self.cargar_datos_en_tabla()

    def _get_next_id(self):
        """Genera el siguiente ID único para una nueva compra."""
        if not self.compras_data:
            return 1
        return max(int(c["id"]) for c in self.compras_data) + 1

    def crear_ui(self):
        """Crea y organiza la interfaz de usuario para la gestión de compras."""
        # Título
        tk.Label(self.frame, text="Gestión de Compras", font=("Arial", 18, "bold")).pack(pady=10)

        # Contenedor para los campos de entrada
        input_frame = tk.Frame(self.frame)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Fecha:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.fecha_entry = tk.Entry(input_frame)
        self.fecha_entry.grid(row=0, column=1, padx=5, pady=2)

        # Se cambia "Proveedor" por "Sucursal"
        tk.Label(input_frame, text="Sucursal:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.sucursal_entry = tk.Entry(input_frame)
        self.sucursal_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Monto:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=2, sticky="e")
        self.monto_entry = tk.Entry(input_frame)
        self.monto_entry.grid(row=2, column=1, padx=5, pady=2)
        
        # Se cambia "Tipo de Producto" por "Identificador del Producto"
        tk.Label(input_frame, text="Identificador del Producto:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=2, sticky="e")
        self.identificador_producto_entry = tk.Entry(input_frame)
        self.identificador_producto_entry.grid(row=3, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Cliente:", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=2, sticky="e")
        self.cliente_entry = tk.Entry(input_frame)
        self.cliente_entry.grid(row=4, column=1, padx=5, pady=2)

        # Botón para agregar compra
        tk.Button(self.frame, text="Agregar Compra", command=self.agregar_compra).pack(pady=5)

        # Tabla (Treeview) con los nombres de columna actualizados
        columns = ("ID", "Fecha", "Sucursal", "Monto", "Identificador Producto", "Cliente")
        self.tabla = ttk.Treeview(self.frame, columns=columns, show="headings")
        for col in columns:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor=tk.CENTER)
        self.tabla.pack(pady=10, fill="both", expand=True)

        # Botón para borrar compra
        tk.Button(self.frame, text="Borrar Compra Seleccionada", command=self.borrar_compra).pack(pady=5)

        # Botón para volver
        tk.Button(self.frame, text="Volver al Menú Principal", command=self.volver_callback).pack(pady=20)
    
    def agregar_compra(self):
        """Función para agregar una nueva compra a los datos y a la tabla."""
        fecha = self.fecha_entry.get()
        sucursal = self.sucursal_entry.get()
        monto = self.monto_entry.get()
        identificador_producto = self.identificador_producto_entry.get()
        cliente = self.cliente_entry.get()

        if not all([fecha, sucursal, monto, identificador_producto, cliente]):
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        nueva_compra = {
            "id": self.next_id,
            "fecha": fecha,
            "sucursal": sucursal,
            "monto": monto,
            "identificador_producto": identificador_producto,
            "cliente": cliente
        }
        self.compras_data.append(nueva_compra)
        save_data(DATA_FILE, self.compras_data, FIELDNAMES)
        self.tabla.insert("", "end", values=(self.next_id, fecha, sucursal, monto, identificador_producto, cliente))
        self.next_id += 1
        self.limpiar_campos()
        messagebox.showinfo("Compra Agregada", "La compra se ha guardado correctamente.")

    def borrar_compra(self):
        """Función para borrar la compra seleccionada de los datos y la tabla."""
        selected_item = self.tabla.selection()
        if not selected_item:
            messagebox.showwarning("Ninguna selección", "Por favor, selecciona una compra para borrar.")
            return

        respuesta = messagebox.askyesno("Confirmar borrado", "¿Estás seguro de que quieres borrar la compra seleccionada?")
        if respuesta:
            item_id = self.tabla.item(selected_item, "values")[0]
            self.compras_data = [c for c in self.compras_data if str(c["id"]) != str(item_id)]
            save_data(DATA_FILE, self.compras_data, FIELDNAMES)
            self.tabla.delete(selected_item)
            messagebox.showinfo("Borrado exitoso", "La compra ha sido eliminada.")

    def cargar_datos_en_tabla(self):
        """Carga los datos existentes en el Treeview."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for compra in self.compras_data:
            self.tabla.insert("", "end", values=(
                compra.get("id"),
                compra.get("fecha"),
                compra.get("sucursal"),
                compra.get("monto"),
                compra.get("identificador_producto"),
                compra.get("cliente")
            ))

    def limpiar_campos(self):
        """Limpia los campos de entrada después de agregar una compra."""
        self.fecha_entry.delete(0, tk.END)
        self.sucursal_entry.delete(0, tk.END)
        self.monto_entry.delete(0, tk.END)
        self.identificador_producto_entry.delete(0, tk.END)
        self.cliente_entry.delete(0, tk.END)
