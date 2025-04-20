import bcrypt
from ..connections import get_db

class User:
    @staticmethod
    def create(username, email, password):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO users (username, email, password, role)
                        VALUES (%s, %s, %s, %s)
                    """, (username, email, hashed_password.decode(), 'client'))
                    conn.commit()
            return True
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return False

    @staticmethod
    def find_by_email(email):
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                    return cur.fetchone()
        except Exception as e:
            print(f"Error al buscar usuario: {e}")
            return None


class Product:
    @staticmethod
    def get_all():
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM products")
                    return cur.fetchall()
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []

    @staticmethod
    def find_by_id(product_id):
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
                    return cur.fetchone()
        except Exception as e:
            print(f"Error al buscar producto: {e}")
            return None


class Cart:
    @staticmethod
    def add_product(user_id, product_id):
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT 1 FROM cart WHERE user_id = %s AND product_id = %s
                    """, (user_id, product_id))
                    if cur.fetchone():
                        cur.execute("""
                            UPDATE cart SET quantity = quantity + 1
                            WHERE user_id = %s AND product_id = %s
                        """, (user_id, product_id))
                    else:
                        cur.execute("""
                            INSERT INTO cart (user_id, product_id, quantity)
                            VALUES (%s, %s, 1)
                        """, (user_id, product_id))
                    conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar producto al carrito: {e}")
            return False

    @staticmethod
    def get_cart_items(user_id):
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
                    return cur.fetchall()
        except Exception as e:
            print(f"Error al obtener carrito: {e}")
            return []