from flask import Blueprint, jsonify, request, session
from ..models.models import User, Product, Cart
client_bp = Blueprint('client', __name__)

# Endpoint para registrar un usuario
@client_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validación de campos requeridos
    if not all([username, email, password]):
        return jsonify({'success': False, 'message': 'Faltan campos requeridos.'}), 400

    # Validación de longitud de contraseña
    if len(password) < 8:
        return jsonify({'success': False, 'message': 'La contraseña debe tener al menos 8 caracteres.'}), 400

    # Verificar si el correo ya está registrado
    if User.find_by_email(email):
        return jsonify({'success': False, 'message': 'Este correo ya está registrado.'}), 409

    # Intentar crear el usuario
    if User.create(username, email, password):
        return jsonify({'success': True, 'message': 'Registro exitoso.'}), 201
    else:
        return jsonify({'success': False, 'message': 'Error en el registro.'}), 500


# Endpoint para obtener todos los productos
@client_bp.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = Product.get_all()
        return jsonify({
            'success': True,
            'products': products
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener los productos: {str(e)}'
        }), 500


# Endpoint para agregar un producto al carrito
@client_bp.route('/api/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Debes iniciar sesión para agregar productos.'}), 401

    try:
        if Cart.add_product(user_id, product_id):
            return jsonify({'success': True, 'message': 'Producto agregado al carrito.'}), 200
        else:
            return jsonify({'success': False, 'message': 'Error al agregar producto.'}), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al agregar producto al carrito: {str(e)}'
        }), 500