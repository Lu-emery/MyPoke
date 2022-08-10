#####################################################################
# init.py - arquivo de inicialização do site
#
# Contribuidores: Lucas Emery
#                 Thiago Damasceno
#
# Funcionalidade:
#   Esse arquivo inicializa o site, definindo as blueprints e o banco de dados de usuários
#####################################################################

# Usamos flask para a funcionalidade do site
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from .mypokeAPI import *

# Definimos o banco de dados de usuários como 'users.db'
db = SQLAlchemy()
DB_NAME = "users.db"

# criar_base_usuários(app)
#   cria a base de dados de usuários caso ela não exista
def criar_base_usuarios(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('BD Criado!')

# criar_app()
#   inicializa o site
#   Saída: a aplicação do site
def criar_app():
    # Criamos o app e definimos as configurações iniciais
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Stop right there, criminal scum!'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializamos a aplicação do site
    db.init_app(app)
    
    # Registramos as blueprints do site
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # Criamos a base de usuários e inicializamos o gerenciador de login
    from .models import User
    criar_base_usuarios(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
