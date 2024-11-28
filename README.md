## Instalar / Activar myvenv
```
python -m venv myvenv
myvenv\Scripts\activate
```
## Importar / Instalar requirements
```
pip freeze > requirements.txt
pip install -r requirements.txt
```
## Generar aplicacion
```
pyinstaller --onefile --noconsole --name "ESCANER AT" --icon "./img/apuesta_total.ico" --add-data "./img/logo_apuesta_total.png;img" --add-data "./img/apuesta_total.ico;img" start.py
```

## Actualizar aplicacion
```
pyinstaller "ESCANER AT.spec"
```