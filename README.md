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
python build.py
```
## Generar una nueva rama
```
git checkout main
git pull origin main
git checkout -b v1.3.0
git push -u origin v1.3.0
```