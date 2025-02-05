from flask import Flask, request, jsonify
from config import Config
from routes.products_routes import products_bp
from controllers.validation_controllers import login, access
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# Configuración de CORS
cors = CORS(app, resources={r"/api/*": {"origins": "https://www.example.com"}}, methods=['GET', 'POST'])

# Middleware para limitar métodos HTTP
@app.before_request
def limit_http_methods():
    if request.method not in ['GET', 'POST']:
        return jsonify({"message": "Method Not Allowed"}), 405

# Middleware para limitar el dominio de acceso
@app.after_request
def limit_access_domain(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://www.example.com'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Configuración de rutas
app.register_blueprint(products_bp, url_prefix='/api/v1/service')

# Ruta GET para mostrar la página de inicio de sesión
@app.route('*', methods=['GET'])
def show_login():
    return login()

# Ruta POST para procesar el inicio de sesión y generar un token de acceso
@app.route('/access', methods=['POST'])
def process_access():
    return access()

if __name__ == '__main__':
    app.run(port=app.config['PORT'])
