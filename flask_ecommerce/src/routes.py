from flask import Blueprint, request, jsonify
from src.models.users import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/')
def home():
    return "¡Flask + PostgreSQL funciona!"

@user_bp.route('/login',methods=['POST'])
def postlogin():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos JSON"}), 400
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    try:
        USER = User.user_by_login_password(email, password)
        if USER:
            return jsonify({"message": "Login exitoso", "user": USER})
        return jsonify({"error": "Credenciales inválidas"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    #USER = user.user_by_login_password(email,password)
    #email = request.from.get('email')
    #password = request.from.get('password')
    #return f"datos de usuario:{USER}" 

@user_bp.route('/register', methods=['POST'])  # Cambiado a solo POST
def postregister():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos JSON"}), 400
        
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    
    # Usar la clase User para el registro
    result = User.register(username, email, password)
    status_code = 201 if result['success'] else 400
    return jsonify(result), status_code