from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "users.db"

def criar_base_usuarios(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('BD Criado!')

def criar_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Stop right there, criminal scum!'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User
    criar_base_usuarios(app)

    return app
