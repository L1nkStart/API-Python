from flask import Blueprint, jsonify, request
from db import get_connection

products_bp = Blueprint('products_bp', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PRODUCTOS")  
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    products_list = [dict(zip([column[0] for column in cursor.description], row)) for row in products]
    return jsonify(products_list)

@products_bp.route('/', methods=['POST'])
def create_product():
    # data = request.get_json()
    # connection = get_connection()
    # cursor = connection.cursor()
    # # Ajusta la consulta según tu tabla y datos
    # cursor.execute("INSERT INTO Products (name, price) VALUES (?, ?)", (data['name'], data['price']))
    # connection.commit()
    # cursor.close()
    # connection.close()
    return jsonify({"message": "Producto creado"})
