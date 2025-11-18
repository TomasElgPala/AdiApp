import tkinter as tk
from tkinter import ttk, messagebox
# Importamos BG_MODULO y FG_PRIMARY, aunque ahora usamos estilos específicos para el look blanco
from estilos import FONT_BASE, FONT_BUTTON, COLOR_ACCENT 
from PIL import Image, ImageTk # Necesario para manejar imágenes

# Variable global para evitar que la imagen sea eliminada por el garbage collector
_logo_login_ref = None 

class LoginUI:
    """Interfaz de usuario para la pantalla de inicio de sesión, con estilo moderno."""
    def __init__(self, root, success_callback):
        self.root = root
        self.success_callback = success_callback
        
        # El frame principal debe usar el estilo 'TFrame' por defecto, que es BG_PRIMARY (blanco/gris)
        # Esto asegura que el fondo de la 'tarjeta' blanca se destaque sobre la imagen de fondo.
        self.frame = ttk.Frame(root, style="TFrame") 
        self.frame.pack(fill="both", expand=True) 
        
        # Quitamos el messagebox.showinfo/showerror ya que no funciona correctamente en algunos entornos.
        self.error_label = ttk.Label(self.frame, text="", style="Error.TLabel")
        self.error_label.pack_forget()

        self.crear_ui()

    def crear_ui(self):
        """Crea y organiza la interfaz de usuario de login, centrada en un contenedor blanco."""
        global _logo_login_ref
        
        # 🌟 MODIFICACIÓN CLAVE: Usamos Login.TFrame (Fondo Blanco) y borde redondeado
        # Usamos tk.Frame y un borde para simular un 'card' limpio.
        login_container = tk.Frame(self.frame, bg="white", padx=50, pady=40, 
                                highlightbackground=COLOR_ACCENT, highlightthickness=1) 
        login_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # --- NUEVO: Agregar Logo Arriba del Título ---
        try:
            img = Image.open("logo_three_stripes.png")
            img = img.resize((80, 50), Image.Resampling.LANCZOS) # Tamaño un poco más grande
            _logo_login_ref = ImageTk.PhotoImage(img) 
            
            # Label para mostrar la imagen (fondo blanco de la tarjeta)
            lbl_logo = tk.Label(login_container, image=_logo_login_ref, bg="white")
            lbl_logo.pack(pady=(0, 10))
        except Exception:
            # Si el logo no se encuentra, mostramos un mensaje alternativo o nada
            print("Advertencia: No se encontró 'logo_three_stripes.png'.")
        # ---------------------------------------------

        # Usamos un título con estilo Login.TLabel (negro sobre blanco)
        ttk.Label(login_container, text="INICIAR SESIÓN", font=("Segoe UI", 20, "bold"), style="Login.TLabel")\
            .pack(pady=(10, 30))
        
        # Campo para mostrar errores
        self.error_label = ttk.Label(login_container, text="", style="Error.TLabel")
        self.error_label.pack(pady=(0, 15))

        # --- Campos de Entrada ---
        
        # Etiqueta de Usuario (style="TLabel" usa texto negro sobre fondo BG_PRIMARY/Blanco)
        ttk.Label(login_container, text="Nombre de Usuario:", font=FONT_BASE, style="Login.TLabel").pack(anchor='w', pady=(5, 0))
        self.usuario_entry = ttk.Entry(login_container, width=35, style="Login.TEntry")
        self.usuario_entry.pack(pady=(5, 10))

        # Etiqueta de Contraseña
        ttk.Label(login_container, text="Contraseña:", font=FONT_BASE, style="Login.TLabel").pack(anchor='w', pady=(5, 0))
        self.contrasena_entry = ttk.Entry(login_container, width=35, show="*", style="Login.TEntry")
        self.contrasena_entry.pack(pady=(5, 15))
        
        # 🌟 MODIFICACIÓN CLAVE: Botón de Login (Usamos Accent.TButton: Fondo Negro, Letra Blanca)
        ttk.Button(login_container, text="ACCEDER AL SISTEMA", command=self.attempt_login, style="Accent.TButton")\
            .pack(pady=(20, 10), fill='x')
            
    def display_error(self, message):
        """Muestra un mensaje de error sin usar messagebox."""
        self.error_label.config(text=message, style="Error.TLabel")
        self.error_label.pack(pady=(0, 15))
        
    def attempt_login(self):
        """Intenta autenticar al usuario."""
        
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()
        
        # Limpiamos errores previos
        self.error_label.config(text="")
        
        # *** Lógica de Autenticación Hardcodeada ***
        if usuario == "admin" and contrasena == "1234":
            # Si es exitoso
            # Usamos el color de acento azul para una confirmación rápida
            self.error_label.config(text="Inicio de sesión exitoso.", foreground=COLOR_ACCENT)
            
            # Esperamos un momento antes de cambiar de pantalla para que el usuario vea el mensaje
            self.root.after(500, self._proceed_to_main_menu) 
        else:
            # Si hay error
            self.display_error("❌ Usuario o contraseña incorrectos.")
            self.contrasena_entry.delete(0, tk.END) # Limpia el campo de contraseña
            
    def _proceed_to_main_menu(self):
        """Función interna para completar la transición."""
        self.frame.destroy() 
        self.success_callback() 
