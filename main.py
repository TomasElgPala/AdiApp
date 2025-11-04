import tkinter as tk
from tkinter import ttk 
from PIL import Image, ImageTk
# 🌟 Importamos el nuevo módulo de Login
from login import LoginUI 
from compras import ComprasUI 
from empleados import EmpleadosUI 
from estilos import configure_styles, add_logo_header, COLOR_ACCENT, BG_PRIMARY

class MainApp:
    """Clase principal de la aplicación, maneja la navegación entre módulos."""
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal de Gestión")
        
        # Aplicar estilos ttk al inicio
        configure_styles(root)
        
        # 🌟 LÍNEA CLAVE: Pantalla completa (Full Screen) 🌟
        self.root.attributes('-fullscreen', True) 
        
        self.background_image = None 
        self.background_label = None
        self.header_frame = None # Nuevo atributo para el encabezado

        # Configuración inicial del fondo
        self._setup_background()
        
        # Vincula el evento de redimensionamiento
        self.root.bind('<Configure>', self.on_resize)
        
        # Opcional: Para salir de pantalla completa con la tecla ESC
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        # Al inicio, mostramos la pantalla de login.
        self.show_login() 

    def exit_fullscreen(self, event):
        """Permite salir de pantalla completa al presionar ESC."""
        self.root.attributes('-fullscreen', False)

    def on_resize(self, event):
        """Vuelve a cargar y redimensiona el fondo cuando la ventana cambia de tamaño."""
        current_width = self.root.winfo_width()
        current_height = self.root.winfo_height()
        
        if current_width > 0 and current_height > 0:
            self._load_and_place_background(current_width, current_height)

    def _load_and_place_background(self, width, height):
        """Carga, redimensiona y coloca la imagen de fondo."""
        try:
            image = Image.open("fondo_adidas.jpg")
            image_resized = image.resize((width, height), Image.Resampling.LANCZOS)
            
            self.background_image = ImageTk.PhotoImage(image_resized)
            
            if self.background_label:
                self.background_label.config(image=self.background_image)
            else:
                self.background_label = tk.Label(self.root, image=self.background_image)
                self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

            self.background_label.lower() 
            
        except FileNotFoundError:
            # Si no hay imagen, asegura un fondo negro
            if not self.background_label:
                self.background_label = tk.Label(self.root, bg="black")
                self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            print("Error: No se encontró la imagen 'fondo_adidas.jpg'. Usando fondo negro.")
        except Exception as e:
            print(f"Error al redimensionar la imagen: {e}")

    def _setup_background(self):
        """Prepara el fondo en el inicio."""
        self.root.update_idletasks() 
        self._load_and_place_background(self.root.winfo_width(), self.root.winfo_height())
        
    def limpiar_frame(self):
        """Limpia todos los widgets excepto la etiqueta de fondo y el frame del header."""
        for widget in self.root.winfo_children():
            # No destruir el fondo ni el frame del header si existe
            if widget is self.background_label or widget is self.header_frame: 
                widget.lift() # Asegura que el header y el fondo se mantengan
                continue
            widget.destroy()

    # --- FUNCIÓN PARA MOSTRAR LOGIN ---
    def show_login(self):
        """Muestra la pantalla de inicio de sesión."""
        self.limpiar_frame()
        # Destruir el header si existe al ir a Login
        if self.header_frame:
            self.header_frame.destroy()
            self.header_frame = None
        # Inicia la interfaz de Login. Si es exitoso, llama a show_main_menu
        LoginUI(self.root, success_callback=self.show_main_menu) 
    # --- FIN FUNCIÓN ---

    # --- FUNCIONES PARA MOSTRAR LOS MÓDULOS ---

    def show_main_menu(self):
        """Limpia la pantalla y muestra el header y los botones del menú principal."""
        self.limpiar_frame()
        
        # Destruir el header si existe (aunque limpiar_frame ya lo maneja, es más seguro)
        if self.header_frame:
             self.header_frame.destroy()
             self.header_frame = None
        
        # add_logo_header ya crea y empaqueta su propio Frame por defecto
        self.header_frame = add_logo_header(self.root, "MENÚ PRINCIPAL DE GESTIÓN")
        self.header_frame.pack(fill='x', side='top') # Asegura que esté en la parte superior
        self.header_frame.lift() # Asegura que esté encima de todo

        self._setup_buttons()

    def show_compras(self):
        """Función que inicia la interfaz de ComprasUI."""
        self.limpiar_frame()
        # Destruir el header cuando entras a un módulo
        if self.header_frame:
            self.header_frame.destroy()
            self.header_frame = None
        ComprasUI(self.root, volver_callback=self.show_main_menu) 

    def show_empleados(self): 
        """Función que inicia la interfaz de EmpleadosUI."""
        self.limpiar_frame()
        # Destruir el header cuando entras a un módulo
        if self.header_frame:
            self.header_frame.destroy()
            self.header_frame = None
        EmpleadosUI(self.root, volver_callback=self.show_main_menu) 

    def show_otro_modulo(self): 
        """Función para un módulo de ejemplo."""
        self.limpiar_frame()
        if self.header_frame:
            self.header_frame.destroy()
            self.header_frame = None

        # Contenedor con fondo blanco/claro (BG_PRIMARY)
        temp_frame = ttk.Frame(self.root, style="TFrame")
        temp_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=200)

        # Usamos TLabel para texto negro sobre fondo claro
        label_temp = ttk.Label(temp_frame, text="MÓDULO FUTURO EN CONSTRUCCIÓN", font=('Segoe UI', 18, 'bold'), style="TLabel")
        label_temp.pack(pady=30)
        
        # Botón de volver usando Accent.TButton (Negro/Blanco)
        ttk.Button(temp_frame, text="< Volver al Menú", command=self.show_main_menu, style="Accent.TButton").pack(pady=10, ipadx=10)
        
    # --- CONFIGURACIÓN DE BOTONES DEL MENÚ PRINCIPAL ---

    def _setup_buttons(self):
        """Crea y coloca los cuatro botones principales en una tarjeta de fondo claro."""
        
        # 🌟 MODIFICACIÓN CLAVE: Cambiamos el estilo de "Modulo.TFrame" (negro) a "TFrame" (claro)
        # Usamos tk.Frame para tener control del color de fondo si es necesario
        button_container = tk.Frame(
            self.root, 
            bg=BG_PRIMARY, # Usamos el color claro BG_PRIMARY
            padx=40, 
            pady=30,
            highlightbackground=COLOR_ACCENT, 
            highlightthickness=1 # Agregamos un borde sutil azul
        ) 
        button_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        button_container.lift()
        
        # Título de la tarjeta (opcional)
        ttk.Label(button_container, text="SELECCIONE UN MÓDULO", font=('Segoe UI', 14, 'bold'), style="TLabel").pack(pady=(0, 20))
        
        # Usaremos el estilo 'Accent.TButton' (Fondo Negro, Letra Blanca) para los botones, 
        # ya que son las acciones principales.
        
        # Botón 1: Compras
        btn_compras = ttk.Button(
            button_container, 
            text="🛒 Gestión de Compras", 
            command=self.show_compras, 
            style="Accent.TButton", # <--- ¡Aquí está el cambio!
            width=30
        )
        btn_compras.pack(pady=10) 

        # Botón 2: Empleados
        btn_empleados = ttk.Button(
            button_container, 
            text="🧑‍💼 Gestión de Empleados", 
            command=self.show_empleados, 
            style="Accent.TButton", # Fondo Negro, Letra Blanca
            width=30
        )
        btn_empleados.pack(pady=10)

        # Botón 3: Otro Módulo
        btn_otro = ttk.Button(
            button_container, 
            text="⚙️ Otro Módulo / Configuración", 
            command=self.show_otro_modulo, 
            style="Accent.TButton", # Fondo Negro, Letra Blanca
            width=30
        )
        btn_otro.pack(pady=10)
        
        # Botón de Salida (Usamos el estilo Accent.TButton para consistencia)
        btn_exit = ttk.Button(
            button_container, 
            text="❌ Salir de la Aplicación", 
            command=self.root.destroy, # Función para cerrar la app
            style="Accent.TButton", # Fondo Negro, Letra Blanca
            width=30
        )
        btn_exit.pack(pady=(20, 0)) # Más espacio arriba

# --- Bucle Principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
