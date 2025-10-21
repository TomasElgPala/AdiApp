import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# === COLORES ADIDAS ===
BG_PRIMARY = "#F7F7F7"       # Fondo de la aplicación principal (gris/blanco roto)
BG_MODULO = "#000000"        # Fondo sólido negro para módulos (Empleados y Compras)
FG_PRIMARY = "#000000"       # Texto principal (negro)
COLOR_ACCENT = "#0C2340"     # Azul oscuro Adidas para headers
COLOR_ACCENT_LIGHT = "#1C3A63"
COLOR_TEXT_BUTTON_MAIN = "#FFFFFF" # Texto de botones principales (blanco)
COLOR_TEXT_BUTTON_MODULO = "#000000" # Texto de botones del módulo (negro)

# === FUENTES ===
FONT_BASE = ("Segoe UI", 11)
FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_BUTTON = ("Segoe UI", 12, "bold")

_logo_image_ref = None

def configure_styles(root):
    """Aplica el estilo general tipo Adidas, incluyendo los nuevos estilos de botones."""
    style = ttk.Style(root)

    # Estilos Base
    root.configure(bg=BG_PRIMARY)
    style.configure(".", background=BG_PRIMARY, foreground=FG_PRIMARY, font=FONT_BASE)

    # Estilos TFrame (Usados en main.py y los módulos)
    style.configure("TFrame", background=BG_PRIMARY)
    style.configure("Modulo.TFrame", background=BG_MODULO) # Fondo negro para módulos

    # Estilos TLabel
    style.configure("TLabel", background=BG_PRIMARY, foreground=FG_PRIMARY)
    style.configure("Title.TLabel", background=COLOR_ACCENT, foreground="white", font=FONT_TITLE)
    style.configure("Modulo.TLabel", background=BG_MODULO, foreground="white") # Texto blanco sobre fondo negro

    # ------------------
    # ESTILOS DE BOTONES
    # ------------------
    
    # 1. Botones del Menú Principal (Main.TButton: Fondo Negro, Texto Blanco)
    style.configure("Main.TButton",
                    font=FONT_BUTTON,
                    foreground=COLOR_TEXT_BUTTON_MAIN,
                    background=BG_MODULO, # <-- Esto es NEGRO
                    padding=10,
                    borderwidth=0)
    style.map("Main.TButton",
              background=[('active', COLOR_ACCENT_LIGHT)], 
              relief=[('pressed', 'sunken')])

    # 2. Botones dentro de los Módulos (Modulo.TButton: Fondo Blanco, Texto Negro)
    style.configure("Modulo.TButton",
                    font=FONT_BUTTON,
                    foreground=COLOR_TEXT_BUTTON_MODULO, 
                    background="white", 
                    padding=10,
                    borderwidth=0)
    style.map("Modulo.TButton",
              background=[('active', "#EAEAEA")], 
              relief=[('pressed', 'sunken')])
              
    # 3. Estilo del Treeview
    style.configure("Treeview.Heading",
                    font=("Segoe UI", 11, "bold"),
                    background=COLOR_ACCENT,
                    foreground="white",
                    relief="flat")
    style.map("Treeview.Heading", background=[('active', COLOR_ACCENT_LIGHT)])
    style.configure("Treeview",
                    background="white",
                    foreground=FG_PRIMARY,
                    fieldbackground="white",
                    rowheight=28,
                    borderwidth=0)

def add_logo_header(parent, title_text, logo_path="logo_three_stripes.png"):
    """Crea el encabezado azul oscuro con el logo y el título."""
    global _logo_image_ref 

    header = tk.Frame(parent, bg=COLOR_ACCENT, height=80)
    header.pack(fill='x', pady=(0, 20))

    try:
        img = Image.open(logo_path)
        img = img.resize((60, 40), Image.Resampling.LANCZOS)
        _logo_image_ref = ImageTk.PhotoImage(img) 
        
        lbl_logo = tk.Label(header, image=_logo_image_ref, bg=COLOR_ACCENT)
        lbl_logo.place(x=20, y=20)
    except Exception:
        # Dibujar líneas blancas si el logo no se encuentra
        for i in range(3):
            tk.Frame(header, bg="white", width=8, height=35).place(x=20 + i * 12, y=20)

    title_label = ttk.Label(header, text=title_text, style="Title.TLabel")
    title_label.place(relx=0.5, rely=0.5, anchor='center')

    return header