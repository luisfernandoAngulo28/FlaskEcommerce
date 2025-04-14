#--------------------------------------------------------------------------------------------------

import psycopg2
from psycopg2 import DatabaseError

#--------------------------------------------------------------------------------------------------
try:
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='12345678',
        database='BDEcommerce'
    )
    connection.autocommit = True
    print("Conexión exitosa.")

except DatabaseError as ex:
    print("Error durante la conexión: {}".format(ex))
#--------------------------------------------------------------------------------------------------
def db_register(query=None, params=None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error en db_register: {e}")
        return False
#--------------------------------------------------------------------------------------------------

def db_fetchall(query = None):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#--------------------------------------------------------------------------------------------------

def db_fetchone(query, values=None):   
    cursor = connection.cursor()
    cursor.execute(query, values)
    result = cursor.fetchone()
    connection.commit()
    cursor.close()
    return result

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
