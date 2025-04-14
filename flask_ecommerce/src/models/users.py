from src.connections.connections import db_register, db_fetchone
#from flask import request
#from connections.connections import db_fetchone, db_register
import bcrypt

class User:
    @classmethod
    def user_by_login_password(cls, email=None, password=None):
        """
        Busca un usuario por email y contraseña (hasheada).
        Retorna el usuario si existe, None si no.
        """
        try:
            user_data = db_fetchone(
                "SELECT * FROM users WHERE email = %s",
                (email,)
            )

            if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
                return user_data
            return None
        except Exception as e:
            print(f"Error en user_by_login_password: {str(e)}")
            return None

    @classmethod
    def register(cls, username, email, password):
        """
        Registra un nuevo usuario.
        Retorna dict con {success, msg}.
        """
        if len(password) < 8:
            return {
                'success': False,
                'msg': 'La contraseña debe tener al menos 8 caracteres.'
            }

        try:
            # Verifica si ya existe un usuario con ese email
            existing_user = db_fetchone(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )

            if existing_user:
                return {
                    'success': False,
                    'msg': 'Este correo electrónico ya está registrado.'
                }

            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            success = db_register(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )

            if success:
                return {
                    'success': True,
                    'msg': 'Registro exitoso. Ahora puedes iniciar sesión.'
                }
            else:
                return {
                    'success': False,
                    'msg': 'Error al insertar usuario en base de datos.'
                }

        except Exception as e:
            print(f"Error en registro: {str(e)}")
            return {
                'success': False,
                'msg': 'Error en el servidor al registrar usuario.'
            }