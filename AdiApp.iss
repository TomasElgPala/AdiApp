; Script generado para Inno Setup Compiler por Gemini
; Basado en la estructura de archivos proporcionada

[Setup]
; --- INFORMACIÓN GENERAL DEL INSTALADOR ---
; Reemplaza los valores entre <> con tus datos
AppName=Mi Aplicación Adidas
AppVersion=1.0.0
AppPublisher=Tu Nombre o Empresa
AppPublisherURL=
AppSupportURL=
AppUpdatesURL=
DefaultDirName={autopf}\Mi Aplicacion Adidas ; Ruta de instalación por defecto
DefaultGroupName=Mi Aplicación Adidas      ; Nombre del grupo en el menú inicio
OutputBaseFilename=setup_app_adidas_1.0

[Files]
; --- ARCHIVO EJECUTABLE PRINCIPAL (CORREGIDO) ---
; Apunta directamente a 'main.exe' en el directorio donde está el script .iss
Source: "main.exe"; DestDir: "{app}"

; --- ARCHIVOS DE DATOS PRINCIPALES ---
; Estos archivos también deben estar en el mismo directorio
Source: "adidas.db"; DestDir: "{app}"
Source: "compras.csv"; DestDir: "{app}"
Source: "empleados.csv"; DestDir: "{app}"
Source: "fondo_adidas.jpg"; DestDir: "{app}"
Source: "logo_three_stripes.png"; DestDir: "{app}"
Source: "produccion.db"; DestDir: "{app}"
Source: "README.md"; DestDir: "{app}"

; --- ARCHIVOS .PY DE REFERENCIA O BIBLIOTECAS ---
; Generalmente, los archivos .py no son necesarios si usas --onefile, 
; pero si usaste --onedir o quieres incluirlos por si acaso:
; Source: "compras.py"; DestDir: "{app}"
; Source: "data_manager.py"; DestDir: "{app}"
; Source: "empleados.py"; DestDir: "{app}"
; Source: "estilos.py"; DestDir: "{app}"
; Source: "legal.py"; DestDir: "{app}"
; Source: "login.py"; DestDir: "{app}"
; Source: "main.py"; DestDir: "{app}"
; Source: "produccion.py"; DestDir: "{app}"


[Icons]
; --- ACCESOS DIRECTOS ---
; Crear un acceso directo en el escritorio

; Crear un acceso directo en el menú de inicio
Name: "{group}\Ejecutar Mi Aplicación Adidas"; Filename: "{app}\main.exe"
Name: "{group}\Desinstalar Mi Aplicación Adidas"; Filename: "{uninstallexe}"


[Run]
; (Opcional) Iniciar la aplicación después de la instalación
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,Mi Aplicación Adidas}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; (Opcional) Acciones a realizar al desinstalar
