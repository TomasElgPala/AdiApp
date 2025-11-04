import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# --- Definición de Colores y Fuentes ---
COLOR_ACCENT = "#005aab"  # Azul oficial/de acento de Adidas
BG_PRIMARY = "#FFFFFF"     # Fondo principal (Blanco para un look limpio)
FG_PRIMARY = "#000000"     # Color de texto principal (Negro)
BG_MODULO = "#F5F5F5"      # Fondo para contenedores modulares (Gris muy claro)
COLOR_ERROR = "#FF0000"    # Color para mensajes de error

FONT_BASE = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 12, "bold")

# Variable global para evitar que la imagen sea eliminada por el garbage collector
_logo_header_ref = None

# --- Función de Configuración de Estilos ---
def configure_styles(root):
    """Configura los estilos Ttk basados en el esquema de color de Adidas."""
    style = ttk.Style(root)
    
    # Fuentes y opciones por defecto
    style.configure('.', font=FONT_BASE, background=BG_PRIMARY, foreground=FG_PRIMARY)
    
    # Estilo base del Frame (Fondo claro para la mayoría de las UI)
    style.configure("TFrame", background=BG_PRIMARY)
    
    # Estilo de Módulo (Fondo gris claro para áreas de contenido)
    style.configure("Modulo.TFrame", background=BG_MODULO)
    
    # ----------------------------------------------------
    # 🌟 NUEVOS ESTILOS DE ENCABEZADO Y LOGIN LIMPIO (Blanco/Negro)
    # ----------------------------------------------------
    
    # Estilo de Login Card (similar a TFrame, pero para la tarjeta de Login)
    style.configure("Login.TFrame", background=BG_PRIMARY)
    
    # Estilo de Label (Texto Negro sobre fondo Claro)
    style.configure("TLabel", background=BG_PRIMARY, foreground=FG_PRIMARY)
    style.configure("Login.TLabel", background=BG_PRIMARY, foreground=FG_PRIMARY)
    
    # Estilo de Label para Módulos (Texto Negro sobre fondo Gris Claro)
    style.configure("Modulo.TLabel", background=BG_MODULO, foreground=FG_PRIMARY)

    # Estilo de Error
    style.configure("Error.TLabel", background=BG_PRIMARY, foreground=COLOR_ERROR)
    
    # ----------------------------------------------------
    # Estilos de Botones
    # ----------------------------------------------------
    
    # 1. Accent Button (Botón de Acción Principal: Fondo Negro, Letra Blanca)
    style.configure("Accent.TButton", 
                    font=FONT_BUTTON,
                    foreground=FG_PRIMARY,    # Letra Blanca
                    background=FG_PRIMARY,    # Fondo Negro
                    padding=(15, 10))
    style.map("Accent.TButton",
              foreground=[('pressed', FG_PRIMARY), ('active', BG_PRIMARY)],
              background=[('pressed', COLOR_ACCENT), ('active', FG_PRIMARY)])

    # 2. Modulo Button (Botón Estándar: Fondo Blanco, Letra Negra)
    # Lo hemos renombrado a 'Standard.TButton' para mayor claridad
    style.configure("Standard.TButton", 
                    font=FONT_BUTTON,
                    foreground=FG_PRIMARY,    # Letra Negra
                    background=BG_PRIMARY,    # Fondo Blanco
                    padding=(15, 10))
    style.map("Standard.TButton",
              foreground=[('pressed', BG_PRIMARY), ('active', FG_PRIMARY)],
              background=[('pressed', COLOR_ACCENT), ('active', BG_MODULO)])
              
    # 3. Header Button (Botón para el encabezado: Fondo Transparente/Claro, Letra Negra)
    style.configure("Header.TButton",
                    font=FONT_BUTTON,
                    foreground=FG_PRIMARY,
                    background=BG_PRIMARY,
                    bordercolor=BG_PRIMARY)
    style.map("Header.TButton",
              foreground=[('active', COLOR_ACCENT)], # Azul al pasar el ratón
              background=[('active', BG_PRIMARY)])

    # ----------------------------------------------------
    # Estilo de Entradas de Texto (Para Login)
    # ----------------------------------------------------
    style.configure("Login.TEntry", 
                    fieldbackground=BG_MODULO,  # Fondo de campo gris muy claro
                    foreground=FG_PRIMARY,      # Texto negro
                    bordercolor=COLOR_ACCENT,   # Borde azul (no siempre visible, depende del SO)
                    relief="flat")
    style.map("Login.TEntry", 
              fieldbackground=[('focus', BG_PRIMARY)],
              bordercolor=[('focus', COLOR_ACCENT)])


# --- Función para crear el Encabezado ---
def add_logo_header(parent, title, back_command=None):
    """
    Crea un encabezado de aplicación limpio con logo, título y botón de retroceso opcional.
    El fondo del encabezado ahora es BLANCO.
    """
    global _logo_header_ref
    
    # 🌟 MODIFICACIÓN CLAVE: Fondo del Header es BLANCO (BG_PRIMARY)
    header_frame = ttk.Frame(parent, style="TFrame", padding=(20, 10)) 
    header_frame.columnconfigure(1, weight=1) # Columna central expandible
    
    # 1. Logo (Columna 0)
    try:
        img = Image.open("logo_three_stripes.png")
        img = img.resize((60, 40), Image.Resampling.LANCZOS)
        _logo_header_ref = ImageTk.PhotoImage(img) 
        
        lbl_logo = tk.Label(header_frame, image=_logo_header_ref, bg=BG_PRIMARY)
        lbl_logo.grid(row=0, column=0, sticky='w')
    except Exception:
        # Si no se encuentra el logo, usa un texto simple
        lbl_logo = ttk.Label(header_frame, text="ADIDAS", font=("Segoe UI", 16, "bold"), style="TLabel")
        lbl_logo.grid(row=0, column=0, sticky='w')
    
    # 2. Título Central (Columna 1)
    lbl_title = ttk.Label(header_frame, text=title, font=("Segoe UI", 18, "bold"), style="TLabel")
    lbl_title.grid(row=0, column=1, sticky='nsw', padx=20)
    
    # 3. Botón de Volver/Salir (Columna 2)
    if back_command:
        # 🌟 Usamos el estilo Header.TButton (Fondo Blanco, Letra Negra/Azul)
        btn_back = ttk.Button(header_frame, text="← Volver al Menú", command=back_command, style="Header.TButton")
        btn_back.grid(row=0, column=2, sticky='e')
    else:
        # Añadir un botón de salida si es el menú principal, usando Accent.TButton
        btn_exit = ttk.Button(header_frame, text="✕ Salir", command=parent.destroy, style="Accent.TButton")
        btn_exit.grid(row=0, column=2, sticky='e')

    return header_frame
