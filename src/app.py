from flask import Flask
from .admin import admin_bp  # Importa usando ruta relativa
from .api.routes import client_bp  # Importa usando ruta relativa

app = Flask(__name__)
app.secret_key = 'secret_key'

# Registrar blueprints
app.register_blueprint(client_bp, url_prefix="/api/client")
app.register_blueprint(admin_bp, url_prefix="/api/admin")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)