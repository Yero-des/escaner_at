# build.py
import importlib.util
import textwrap
import subprocess

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

# Guardar en version.txt
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
