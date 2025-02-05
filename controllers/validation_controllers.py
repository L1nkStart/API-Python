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
