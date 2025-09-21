import importlib.util
import textwrap
import subprocess
import os

# Cargar VERSION desde start.py
spec = importlib.util.spec_from_file_location("start", "start.py")
start = importlib.util.module_from_spec(spec)
spec.loader.exec_module(start)

version = start.VERSION

# Crear contenido de version.txt
version_info = textwrap.dedent(f"""
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({version.replace('.', ', ')}, 0),
    prodvers=({version.replace('.', ', ')}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'YeroDev'),
        StringStruct(u'FileDescription', u'ESCANER AT'),
        StringStruct(u'FileVersion', u'{version}'),
        StringStruct(u'InternalName', u'ESCANER AT'),
        StringStruct(u'OriginalFilename', u'ESCANER AT.exe'),
        StringStruct(u'ProductName', u'ESCANER AT'),
        StringStruct(u'ProductVersion', u'{version}')])
        ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
""")

with open("version.txt", "w", encoding="utf-8") as f:
    f.write(version_info)

print(f"✅ version.txt generado con la versión {version}")

# Ejecutar PyInstaller automáticamente
subprocess.run([
  "pyinstaller",
  "--onefile",
  "--noconsole",
  "--name", "ESCANER AT",
  "--icon", "./img/apuesta_total.ico",
  "--version-file", "version.txt",
  "--add-data", "./img/logo_apuesta_total.png;img",
  "--add-data", "./img/apuesta_total.ico;img",
  "start.py"
])

print("✅ Ejecutable generado en la carpeta dist/")

# Crear installer.iss para Inno Setup
installer_script = textwrap.dedent(f"""
[Setup]
AppName=Escaner AT
AppVersion={version}
DefaultDirName={{autopf}}\\Escaner_AT
DefaultGroupName=Escaner AT
OutputBaseFilename=Instalador Escaner AT v{version}
SetupIconFile={os.path.join(os.getcwd(), "img", "apuesta_total.ico")}
Compression=lzma2/ultra64
SolidCompression=no

[Files]
Source: "{os.path.join(os.getcwd(), "dist", "ESCANER AT.exe") }"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{os.path.join(os.getcwd(), "build", "*") }"; DestDir: "{{app}}\\recursos"; Flags: recursesubdirs

[Icons]
Name: "{{commondesktop}}\\Escaner AT"; Filename: "{{app}}\\ESCANER AT.exe"; WorkingDir: "{{app}}"
Name: "{{group}}\\Escaner AT"; Filename: "{{app}}\\ESCANER AT.exe"
Name: "{{group}}\\Uninstall Escaner AT"; Filename: "{{uninstallexe}}"
""")

with open("installer.iss", "w", encoding="utf-8") as f:
  f.write(installer_script)

print(f"✅ installer.iss generado con la versión {version}")
print("ℹ️ Ahora puedes abrir 'installer.iss' en Inno Setup y compilar tu instalador.")
