from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from .mypokeAPI import *

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
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User
    criar_base_usuarios(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
