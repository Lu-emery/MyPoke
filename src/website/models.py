#####################################################################
# models.py - arquivo de declaração do banco de dados de usuários
#
# Contribuidores: Lucas Emery
#                 Thiago Damasceno
#
# Funcionalidade:
#   Esse arquivo declara o formato do banco de dados users.db
#####################################################################

from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))
    database = db.Column(db.String(40))
    is_admin = db.Column(db.Boolean, default=False)