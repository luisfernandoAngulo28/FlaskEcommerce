from flask import Flask
from client import client_bp  # Importa desde el paquete src
from admin import admin_bp    # Si tienes blueprint de admin
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost:5432/BDEcommerce'
#db = SQLAlchemy(app)

#from routes import *
# Registra los blueprints
app.register_blueprint(client_bp, url_prefix="/")     # Ruta principal
app.register_blueprint(admin_bp, url_prefix="/admin") # Si aplica


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)