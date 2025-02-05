# Guía para Crear una API con Python y Flask

En este notebook aprenderás a construir una API básica con Flask. 
Este ejemplo incluye configuraciones iniciales, middlewares, manejo de rutas y controladores.


 ## 1. Instalación y Configuración Inicial

 ### Instalar Flask y Flask-CORS
 Ejecuta el siguiente comando en una celda de código o terminal para instalar Flask y Flask-CORS:



```python
pip install flask flask-cors
```

    Requirement already satisfied: flask in c:\users\eduar\appdata\local\programs\python\python312\lib\site-packages (3.0.3)
    Requirement already satisfied: flask-cors in c:\users\eduar\appdata\local\programs\python\python312\lib\site-packages (4.0.1)
    Requirement already satisfied: Werkzeug>=3.0.0 in c:\users\eduar\appdata\local\programs\python\python312\lib\site-packages (from flask) (3.0.3)
    Requirement already satisfied: Jinja2>=3.1.2 in c:\users\eduar\appdata\local\programs\python\python312\lib\site-packages (from flask) (3.1.4)
    Requirement already satisfied: itsdangerous>=2.1.2 in c:\users\eduar\appdata\local\programs\python\python312\lib\site-packages (from flask) (2.2.0)
    Requirement already satisfied: click>=8.1.3 in c:\users\eduar\appdata\local\programs\python\python312\lib\site-packages (from flask) (8.1.7)
    Requirement already satisfied: blinker>=1.6.2 in c:\users\eduar\appdata\local\programs\python\python312\lib\site-packages (from flask) (1.8.2)
    Requirement already satisfied: colorama in c:\users\eduar\appdata\local\programs\python\python312\lib\site-packages (from click>=8.1.3->flask) (0.4.6)
    Requirement already satisfied: MarkupSafe>=2.0 in c:\users\eduar\appdata\local\programs\python\python312\lib\site-packages (from Jinja2>=3.1.2->flask) (2.1.5)
    

    
    [notice] A new release of pip is available: 24.1.2 -> 25.0
    [notice] To update, run: python.exe -m pip install --upgrade pip
    

### Crear Archivos del Proyecto
Vamos a simular la estructura del proyecto.
Puedes crear la estructura manualmente.
En este caso usaremos Python para generar los archivos necesarios.



```python
import os

# Crear la estructura de carpetas
os.makedirs("project/controllers", exist_ok=True)
os.makedirs("project/routes", exist_ok=True)

# Crear archivos vacíos
files = [
    "project/app.py",
    "project/config.py",
    "project/controllers/validation_controllers.py",
    "project/routes/products_routes.py",
]

for file in files:
    with open(file, "w") as f:
        f.write("")

print("Estructura del proyecto creada.")
```

    Estructura del proyecto creada.
    

## 2. Configuración de Flask y Config.py

En el archivo `config.py`, definimos la clase de configuración. 
Aquí incluimos parámetros como el puerto, modo debug, y claves secretas.


```python
class Config:
    PORT = 5000 
    DB_USER = 'sa'
    DB_PORT = 1433
    DB_PASSWORD = ''
    DB_SERVER = 'localhost'
    DB_DATABASE = ''
    DB_SERVER_REMOTO = 'localhost'
    SECRET='vidmr'
```

## 3. Creación de Controladores

En este paso, definimos las funciones para manejar las peticiones relacionadas con el inicio de sesión.



```python
from flask import jsonify, request
from db import get_connection

def login():
    return jsonify({"message": "Mostrar la página de inicio de sesión"})

def access():
    data = request.get_json()
    # Procesar los datos de inicio de sesión y generar un token de acceso
    connection = get_connection()
    cursor = connection.cursor()
    # Ejecuta consultas SQL para la autenticación si es necesario
    cursor.close()
    connection.close()
    return jsonify({"message": "Proceso de acceso", "token": "fake-token"})

```

## 4. Creación de Rutas

Las rutas manejan las peticiones HTTP para la API. 
En este ejemplo, creamos una ruta para listar productos


```python
from flask import Blueprint, jsonify, request
from db import get_connection

products_bp = Blueprint('products_bp', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM MA_PRODUCTOS")  
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    products_list = [dict(zip([column[0] for column in cursor.description], row)) for row in products]
    return jsonify(products_list)

```

## 5. Configuración de la Aplicación Principal

Ahora combinamos todo en `app.py`, donde configuramos Flask, registramos rutas y aplicamos middlewares.



```python
from flask import Flask, request, jsonify
from config import Config
from routes.products_routes import products_bp
from controllers.validation_controllers import login, access
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

```

# Configuración de CORS


```python
cors = CORS(app, resources={r"/api/*": {"origins": "https://www.example.com"}}, methods=['GET', 'POST'])
```

# Middleware para limitar métodos HTTP


```python
@app.before_request
def limit_http_methods():
    if request.method not in ['GET', 'POST']:
        return jsonify({"message": "Method Not Allowed"}), 405
```

# Middleware para limitar el dominio de acceso


```python
@app.after_request
def limit_access_domain(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://www.example.com'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response
```

# Configuración de rutas


```python
app.register_blueprint(products_bp, url_prefix='/api/v1/service')
```

# Ruta GET para mostrar la página de inicio de sesión


```python
@app.route('*', methods=['GET'])
def show_login():
    return login()
```

# Ruta POST para procesar el inicio de sesión y generar un token de acceso


```python
@app.route('/access', methods=['POST'])
def process_access():
    return access()

if __name__ == '__main__':
    app.run(port=app.config['PORT'])
```
