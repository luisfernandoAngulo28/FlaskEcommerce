from flask import Flask
from src.routes import user_bp
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost:5432/BDEcommerce'
#db = SQLAlchemy(app)

#from routes import *
app.register_blueprint(user_bp, url_prefix="/api")


if __name__ == '__main__':
    app.run(debug=True)