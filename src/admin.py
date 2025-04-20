from flask import Blueprint, jsonify, request
from connections import connection  
#from .connections import connection
admin_bp = Blueprint('admin', __name__)

def get_db():
    return connection

# Ruta para el dashboard (estadísticas generales)
@admin_bp.route('/api/admin/dashboard', methods=['GET'])
def dashboard():
    try:
        conn = get_db()
        cur = conn.cursor()

        # Contar productos
        cur.execute("SELECT COUNT(*) AS total_products FROM products")
        total_products = cur.fetchone()[0]

        # Contar usuarios
        cur.execute("SELECT COUNT(*) AS total_users FROM users WHERE role='client'")
        total_users = cur.fetchone()[0]

        # Contar órdenes
        cur.execute("SELECT COUNT(*) AS total_orders FROM orders")
        total_orders = cur.fetchone()[0]

        conn.close()

        # Devolver estadísticas en formato JSON
        return jsonify({
            "success": True,
            "data": {
                "total_products": total_products,
                "total_users": total_users,
                "total_orders": total_orders
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error al cargar el dashboard: {str(e)}"
        }), 500

# Ruta para listar productos
@admin_bp.route('/api/admin/products', methods=['GET'])
def products():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()

        # Convertir los datos en un formato serializable
        products = [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": float(row[3]),
                "stock": row[4],
                "image_url": row[5]
            }
            for row in rows
        ]

        conn.close()

        return jsonify({
            "success": True,
            "data": products
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error al obtener los productos: {str(e)}"
        }), 500

# Ruta para agregar un producto
@admin_bp.route('/api/admin/products/add', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock')
    image_url = data.get('image_url')

    if not all([name, description, price, stock, image_url]):
        return jsonify({
            "success": False,
            "message": "Todos los campos son requeridos."
        }), 400

    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        return jsonify({
            "success": False,
            "message": "El precio y el stock deben ser números válidos."
        }), 400

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO products (name, description, price, stock, image_url) VALUES (%s, %s, %s, %s, %s)",
            (name, description, price, stock, image_url)
        )
        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Producto agregado con éxito."
        }), 201

    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({
            "success": False,
            "message": f"Error al agregar el producto: {str(e)}"
        }), 500

# Ruta para editar un producto
@admin_bp.route('/api/admin/products/edit/<int:id>', methods=['PUT'])
def edit_product(id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock')
    image_url = data.get('image_url')

    if not all([name, description, price, stock, image_url]):
        return jsonify({
            "success": False,
            "message": "Todos los campos son requeridos."
        }), 400

    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        return jsonify({
            "success": False,
            "message": "El precio y el stock deben ser números válidos."
        }), 400

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE products 
            SET name=%s, description=%s, price=%s, stock=%s, image_url=%s 
            WHERE id=%s
            """,
            (name, description, price, stock, image_url, id)
        )
        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Producto actualizado con éxito."
        }), 200

    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({
            "success": False,
            "message": f"Error al actualizar el producto: {str(e)}"
        }), 500

# Ruta para eliminar un producto
@admin_bp.route('/api/admin/products/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id=%s", (id,))
        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Producto eliminado con éxito."
        }), 200

    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({
            "success": False,
            "message": f"Error al eliminar el producto: {str(e)}"
        }), 500