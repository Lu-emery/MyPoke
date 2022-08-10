#####################################################################
# auth.py - arquivo de blueprint de páginas de autenticação
#
# Contribuidores: Lucas Emery
#                 Thiago Damasceno
#
# Funcionalidade:
#   Esse arquivo contém a rota e os chamados de todas as páginas
#   para o banco de dados de autenticação
#####################################################################

# Usamos flask para a funcionalidade do site e werkzeug.security para hash de senhas
from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Caso o usuário já esteja logado, ele é direcionado para a página /home
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        # Caso seja feita uma chamada de login
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember-me')
        
        user = User.query.filter_by(username = username).first()
        if user:
            # Checa-se se o usuário existe no banco de dados
            if check_password_hash(user.password, password):
                # e se a senha está certa
                flash("Login feito com sucesso!", category="SUCCESS")
                if remember == None:
                    login_user(user)
                else:
                    login_user(user, remember=True)
                    
                # então, setamos o usuário da sessão e direcionamos o usuário para /home
                session['username'] = username
                return redirect(url_for('views.home'))
        
        # Tratamento de erros
            else:
                if len(password) > 0:
                    # Senha incorreta
                    flash("Senha incorreta! Tente novamente.", category="ERROR")
                else:
                    # Senha vazia
                    flash("Por favor insira uma senha.", category="ERROR")                    
        else:
            if len(username) > 0:
                # Usuário incorreto
                flash("Não existe usuário com esse nome.", category="ERROR")
            else:
                # Usuário vazio
                flash("Por favor insira um nome de usuário.", category="ERROR")
            if len(password) == 0:
                # Senha vazia (2)
                flash("Por favor insira uma senha.", category="ERROR")
                
    return render_template("login.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Caso seja feita uma chamada de cadastro
        username = request.form.get("username")
        password = request.form.get("password")
        
        if password == "3333":
            # Definimos como administrador, por função de teste, usuários com a senha '3333'
            admin = True
        else:
            admin = False
            
        # Tratamento de erros
        errored = False
        if len(username) < 4:
            # Usuário pequeno de mais
            flash('Nome de usuário deve ter pelo menos 4 caracteres.', category='ERROR')
            errored = True
        if len(password) < 4:
            # Senha pequena de mais
            flash('Senha deve ter pelo menos 4 caracteres.', category='ERROR')
            errored = True
        
        if not errored:
            user = User.query.filter_by(username = username).first()
            if user:
                # Checamos se o usuário já existe
                flash("Usuário com esse nome já existe!", category="ERROR")
            else:
                # Adicionamos o usuário novo no banco de dados
                flash('Conta criada com sucesso!', category='SUCCESS')
                new_user = User(username = username, password = generate_password_hash(password, method='sha256'), is_admin = admin)
                db.session.add(new_user)
                db.session.commit()
                
                # Então, direcionamos o usuário para a página de login
                return redirect(url_for('auth.login'))
            
    return render_template("sign_up.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    # Removemos o usuário da sessão,
    session.pop('username', None)
    # deslogamos o usuário
    logout_user()
    # então direcionamos ele para a página de login
    return redirect(url_for('auth.login'))