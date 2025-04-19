import bcrypt
import numpy as np
import psycopg2
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from psycopg2.extras import RealDictCursor
from sklearn.metrics.pairwise import cosine_similarity
from connections import connection  # Importa tu conexión existente
from sklearn.feature_extraction.text import TfidfVectorizer  # Añade esto al inicio del archivo
from flask import request, jsonify, Blueprint,session
from ..connections import get_db
#client_bp = Blueprint('client', __name__, template_folder='templates/client')
client_bp = Blueprint('client', __name__, template_folder='templates/client')

def get_db():
    # Asumiendo que DB_CONFIG es un diccionario que contiene las credenciales de la DB
    #config = connection.copy()  # Hacemos una copia para evitar modificar el original
    #config.pop('cursor_factory', None)  # Nos aseguramos de que no esté en DB_CONFIG

    #return psycopg2.connect(cursor_factory=RealDictCursor, **config)
    return connection 

client_bp = Blueprint('client', __name__)
def require_login_json():
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Debes iniciar sesión.'
        }), 401  # Unauthorized
    return None

@client_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'success': False, 'message': 'Faltan campos requeridos.'}), 400

    if len(password) < 8:
        return jsonify({'success': False, 'message': 'La contraseña debe tener al menos 8 caracteres.'}), 400

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
                if cur.fetchone():
                    return jsonify({'success': False, 'message': 'Este correo ya está registrado.'}), 409

                cur.execute("""
                    INSERT INTO users (username, email, password, role)
                    VALUES (%s, %s, %s, %s)
                """, (username, email, hashed_password.decode(), 'client'))
                conn.commit()

        return jsonify({'success': True, 'message': 'Registro exitoso.'}), 201

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error en el registro: {str(e)}'}), 500



@client_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'success': False, 'message': 'Correo y contraseña son requeridos.'}), 400

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cur.fetchone()

                if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    return jsonify({
                        'success': True,
                        'message': 'Inicio de sesión exitoso.',
                        'user': {
                            'id': user['id'],
                            'username': user['username'],
                            'email': user['email']
                        }
                    }), 200

                return jsonify({'success': False, 'message': 'Correo o contraseña incorrectos.'}), 401

    except Exception as e:
        return jsonify({'success': False, 'message': 'Error en inicio de sesión: ' + str(e)}), 500


@client_bp.route('/logout', methods=['POST'])  # Mejor usar POST para logout
def logout():
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Has cerrado sesión exitosamente.'
    }), 200

@client_bp.route('/api/products', methods=['GET'])
def get_products():
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM products")
                rows = cur.fetchall()

                # Convertir los datos en un formato serializable
                products = [
                    {
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'price': float(row['price']),
                        'image_url': row['image_url']  # ajusta según tus columnas
                    }
                    for row in rows
                ]

        return jsonify({
            'success': True,
            'products': products
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'No se pudieron cargar los productos.',
            'error': str(e)
        }), 500

@client_bp.route('/api/ranking', methods=['GET'])
def ranking_api():
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, description, price, image_url FROM products")
                all_products = cur.fetchall()

                user_id = session.get("user_id", 1)  # 🔐 Esto es temporal. Idealmente usa un token JWT.
                cur.execute("SELECT product_id FROM cart WHERE user_id = %s", (user_id,))
                cart_product_ids = {row[0] for row in cur.fetchall()}

        if cart_product_ids:
            texts = [f"{prod[1]} {prod[2]}" for prod in all_products]
            product_ids = [prod[0] for prod in all_products]

            vectorizer = TfidfVectorizer(stop_words='spanish')
            tfidf_matrix = vectorizer.fit_transform(texts)

            cart_indices = [i for i, pid in enumerate(product_ids) if pid in cart_product_ids]
            cart_vectors = tfidf_matrix[cart_indices]

            similarity_scores = cosine_similarity(cart_vectors, tfidf_matrix)
            avg_similarity = np.mean(similarity_scores, axis=0)
            ranked_indices = np.argsort(avg_similarity)[::-1]

            recommended = []
            similarity_data = []

            for i in ranked_indices:
                if product_ids[i] not in cart_product_ids:
                    product = all_products[i]
                    recommended.append({
                        'id': product[0],
                        'name': product[1],
                        'description': product[2],
                        'price': float(product[3]),
                        'image_url': product[4],
                        'score': round(float(avg_similarity[i]), 3)
                    })
                if len(recommended) >= 4:
                    break

            mean_score = float(np.max(avg_similarity))
        else:
            recommended = []
            mean_score = 0.0

        return jsonify({
            'success': True,
            'mean_score': mean_score,
            'recommended': recommended
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al generar el ranking.',
            'error': str(e)
        }), 500

@client_bp.route('/api/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart_api(product_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Debes iniciar sesión para agregar productos.'}), 401

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                # Verificar si el producto existe
                cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
                product = cur.fetchone()
                if not product:
                    return jsonify({'success': False, 'message': 'Producto no encontrado.'}), 404

                # Verificar si ya está en el carrito
                cur.execute("""
                    SELECT 1 FROM cart WHERE user_id = %s AND product_id = %s
                """, (user_id, product_id))

                if cur.fetchone():
                    # Ya está: aumentar cantidad
                    cur.execute("""
                        UPDATE cart SET quantity = quantity + 1
                        WHERE user_id = %s AND product_id = %s
                    """, (user_id, product_id))
                else:
                    # No está: insertar nuevo
                    cur.execute("""
                        INSERT INTO cart (user_id, product_id, quantity)
                        VALUES (%s, %s, 1)
                    """, (user_id, product_id))

                conn.commit()

        return jsonify({'success': True, 'message': 'Producto agregado al carrito.'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al agregar producto: {str(e)}'}), 500
    

@client_bp.route('/api/cart', methods=['GET'])
def cart_api():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Debes iniciar sesión para ver el carrito.'}), 401

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT p.name, p.price, c.quantity, 
                           (p.price * c.quantity) AS total_price, c.product_id
                    FROM cart c
                    JOIN products p ON c.product_id = p.id
                    WHERE c.user_id = %s
                """, (user_id,))
                items = cur.fetchall()

        total = sum(item['total_price'] for item in items)

        cart_items = [
            {
                'product_id': item['product_id'],
                'name': item['name'],
                'price': float(item['price']),
                'quantity': item['quantity'],
                'total_price': float(item['total_price'])
            }
            for item in items
        ]

        return jsonify({
            'success': True,
            'cart_items': cart_items,
            'total': round(total, 2)
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al cargar el carrito: {str(e)}'}), 500

@client_bp.route('/api/cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart_api(product_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Debes iniciar sesión para eliminar productos.'}), 401

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s",
                            (user_id, product_id))
                conn.commit()

        return jsonify({'success': True, 'message': 'Producto eliminado del carrito.'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al eliminar el producto: {str(e)}'}), 500
    
@client_bp.route('/checkout', methods=['POST'])
def checkout():
    if not session.get('user_id'):
        return jsonify({"message": "No estás autenticado, por favor inicia sesión"}), 401

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                # Obtener los productos del carrito
                cur.execute("""
                    SELECT p.price, c.quantity
                    FROM cart c
                    JOIN products p ON c.product_id = p.id
                    WHERE c.user_id = %s
                """, (session['user_id'],))
                items = cur.fetchall()

                # Calcular el total de la compra
                total = sum(i['price'] * i['quantity'] for i in items)

                # Insertar la orden en la base de datos
                cur.execute("INSERT INTO orders (user_id, total) VALUES (%s, %s) RETURNING id",
                            (session['user_id'], total))
                order_id = cur.fetchone()['id']

                # Eliminar los productos del carrito después de la compra
                cur.execute("DELETE FROM cart WHERE user_id = %s", (session['user_id'],))
                conn.commit()

        return jsonify({"message": "¡Compra realizada con éxito!", "order_id": order_id}), 200

    except Exception as e:
        return jsonify({"message": f"Error al realizar compra: {str(e)}"}), 500
     
@client_bp.route('/order_summary/<int:order_id>', methods=['GET'])
def order_summary(order_id):
    if not session.get('user_id'):
        return jsonify({"message": "No estás autenticado, por favor inicia sesión"}), 401

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                # Obtener los detalles de la orden
                cur.execute("SELECT * FROM orders WHERE id = %s AND user_id = %s",
                            (order_id, session['user_id']))
                order = cur.fetchone()

        if not order:
            return jsonify({"message": "Orden no encontrada."}), 404

        # Convertir el resultado a un diccionario (si es necesario)
        order_details = {
            "order_id": order["id"],
            "user_id": order["user_id"],
            "total": order["total"],
            "created_at": order["created_at"],  # Asumiendo que 'created_at' es uno de los campos
        }

        return jsonify({"order": order_details}), 200

    except Exception as e:
        return jsonify({"message": f"Error al cargar orden: {str(e)}"}), 500       