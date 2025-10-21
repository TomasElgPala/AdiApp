import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import save_data, load_data
# Importamos BG_MODULO para el fondo negro
from estilos import BG_MODULO, FG_PRIMARY, COLOR_ACCENT, FONT_BASE, FONT_BUTTON, add_logo_header

DATA_FILE = "compras.csv"
FIELDNAMES = ["id", "fecha", "sucursal", "monto", "identificador_producto", "cliente"]

class ComprasUI:
    def __init__(self, root, volver_callback):
        # Crear un frame principal que ocupe todo el root y tenga el fondo negro
        self.frame = ttk.Frame(root, style="Modulo.TFrame") 
        self.frame.pack(fill="both", expand=True) 

        self.volver_callback = volver_callback
        self.compras_data = load_data(DATA_FILE)
        self.next_id = self._get_next_id()
        self.crear_ui()
        self.cargar_datos_en_tabla()

    def _get_next_id(self):
        """Calcula el siguiente ID disponible."""
        if not self.compras_data:
            return 1
        return max(int(c["id"]) for c in self.compras_data) + 1

    def crear_ui(self):
        """Crea y organiza la interfaz de usuario para la gestión de compras, con estilo negro."""
        
        # 🛠️ INICIO DE CORRECCIÓN: Definición de estilos Treeview
        style = ttk.Style(self.frame)
        
        # 1. Definir el estilo principal de la tabla (Treeview) para que no falle.
        # Hereda del estilo base, pero puedes ajustar colores del texto/fondo del contenido.
        style.configure("BlackText.Treeview", 
                        font=("Segoe UI", 10),
                        rowheight=25,
                        fieldbackground="white")
                        
        # 2. Definir el estilo del encabezado (Heading) con texto negro (FG_PRIMARY)
        style.configure("BlackText.Treeview.Heading",
                        font=("Segoe UI", 11, "bold"),
                        background=COLOR_ACCENT, 
                        foreground=FG_PRIMARY,   # Texto del encabezado en NEGRO
                        relief="flat")
        # 🛠️ FIN DE CORRECCIÓN
        
        # Encabezado con el "Logo"
        add_logo_header(self.frame, "Gestión de Compras (Seguimiento de Pedidos)")

        # Contenedor para los campos de entrada (fondo negro)
        input_frame = ttk.Frame(self.frame, style="Modulo.TFrame", padding="15")
        input_frame.pack(pady=15)

        # Labels usan estilo Modulo.TLabel (Texto blanco sobre fondo negro)
        
        # Fila 0
        ttk.Label(input_frame, text="Fecha (DD/MM/YYYY):", font=FONT_BASE, style="Modulo.TLabel").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.fecha_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.fecha_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(input_frame, text="Sucursal:", font=FONT_BASE, style="Modulo.TLabel").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.sucursal_entry = ttk.Entry(input_frame, width=30, style="TEntry")
        self.sucursal_entry.grid(row=0, column=3, padx=10, pady=5)

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
        columns = ("ID", "Fecha", "Sucursal", "Monto", "Identificador Producto", "Cliente")
        
        table_frame = ttk.Frame(self.frame, style="Modulo.TFrame")
        table_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        # 💡 Se asigna el estilo BlackText.Treeview
        self.tabla = ttk.Treeview(table_frame, columns=columns, show="headings", style="BlackText.Treeview")
        
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        vsb.pack(side='right', fill='y')
        self.tabla.configure(yscrollcommand=vsb.set)

        for col in columns:
            self.tabla.heading(col, text=col)
            # El ancho se mantiene en 100 como en tu original.
            self.tabla.column(col, width=100, anchor=tk.CENTER)
            
        self.tabla.pack(side='left', fill="both", expand=True)

        # Botón para volver (Blanco con texto negro)
        ttk.Button(self.frame, text="< Volver al Menú Principal", command=self.volver_callback, style="Modulo.TButton").pack(pady=20, ipadx=10)
    
    def agregar_compra(self):
        """Recoge los datos, valida y agrega una nueva compra."""
        # ... (Lógica sin cambios)
        fecha = self.fecha_entry.get()
        sucursal = self.sucursal_entry.get()
        monto = self.monto_entry.get()
        identificador_producto = self.identificador_producto_entry.get()
        cliente = self.cliente_entry.get()

        if not all([fecha, sucursal, monto, identificador_producto, cliente]):
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        try:
            float(monto)
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido.")
            return

        nueva_compra = {
            "id": str(self.next_id),
            "fecha": fecha,
            "sucursal": sucursal,
            "monto": monto,
            "identificador_producto": identificador_producto,
            "cliente": cliente
        }

        self.compras_data.append(nueva_compra)
        save_data(DATA_FILE, self.compras_data, FIELDNAMES)
        self.cargar_datos_en_tabla()
        self.limpiar_campos()
        self.next_id = self._get_next_id() # Actualiza el ID
        messagebox.showinfo("Éxito", f"Compra {nueva_compra['id']} agregada correctamente.")


    def borrar_compra(self):
        """Elimina la compra seleccionada de la tabla y los datos."""
        # ... (Lógica sin cambios)
        selected_item = self.tabla.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona una compra para borrar.")
            return

        item_data = self.tabla.item(selected_item, 'values')
        compra_id = item_data[0] # El ID es el primer valor

        if messagebox.askyesno("Confirmar Borrado", f"¿Estás seguro de que deseas borrar la compra ID {compra_id}?"):
            # Filtrar la lista de datos para excluir la compra
            self.compras_data = [c for c in self.compras_data if c.get("id") != compra_id]
            
            # Guardar los datos actualizados
            save_data(DATA_FILE, self.compras_data, FIELDNAMES)
            
            # Recargar la tabla
            self.cargar_datos_en_tabla()
            messagebox.showinfo("Éxito", f"Compra ID {compra_id} borrada correctamente.")
            self.next_id = self._get_next_id() # Recalcula el siguiente ID

    def cargar_datos_en_tabla(self):
        """Limpia la tabla y la rellena con los datos actuales."""
        # ... (Lógica sin cambios)
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        # Insertar nuevos datos
        for compra in self.compras_data:
            self.tabla.insert('', 'end', values=(
                compra.get("id"),
                compra.get("fecha"),
                compra.get("sucursal"),
                compra.get("monto"),
                compra.get("identificador_producto"),
                compra.get("cliente")
            ))

    def limpiar_campos(self):
        """Limpia los campos de entrada de la UI."""
        # ... (Lógica sin cambios)
        self.fecha_entry.delete(0, tk.END)
        self.sucursal_entry.delete(0, tk.END)
        self.monto_entry.delete(0, tk.END)
        self.identificador_producto_entry.delete(0, tk.END)
        self.cliente_entry.delete(0, tk.END)