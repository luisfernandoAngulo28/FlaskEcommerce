import psycopg2
from psycopg2 import DatabaseError
from psycopg2.extras import RealDictCursor

# Configuración global de la conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': '12345678',
    'database': 'DataBaseEcommerce',
    'port': 5432,
}

def get_db():
    try:
        return psycopg2.connect(cursor_factory=RealDictCursor, **DB_CONFIG)
    except DatabaseError as ex:
        print(f"Error durante la conexión: {ex}")
        return None

def db_register(query=None, params=None):
    conn = get_db()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
        return True
    except Exception as e:
        print(f"Error en db_register: {e}")
        return False
    finally:
        conn.close()

def db_fetchall(query=None):
    conn = get_db()
    if not conn:
        return []
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error en db_fetchall: {e}")
        return []
    finally:
        conn.close()

def db_fetchone(query=None, values=None):
    conn = get_db()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, values)
            result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Error en db_fetchone: {e}")
        return None
    finally:
        conn.close()