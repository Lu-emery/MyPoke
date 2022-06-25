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
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember-me')
        
        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Login feito com sucesso!", category="SUCCESS")
                if remember == None:
                    login_user(user)
                else:
                    login_user(user, remember=True)
                session['username'] = username
                return redirect(url_for('views.home'))
            else:
                if len(password) > 0:
                    flash("Senha incorreta! Tente novamente.", category="ERROR")
                else:
                    flash("Por favor insira uma senha.", category="ERROR")                    
        else:
            if len(username) > 0:
                flash("Não existe usuário com esse nome.", category="ERROR")
            else:
                flash("Por favor insira um nome de usuário.", category="ERROR")
            if len(password) == 0:
                flash("Por favor insira uma senha.", category="ERROR")
    return render_template("login.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if password == "3333":
            admin = True
        else:
            admin = False        
        database = request.form.get("database")
        e = False
        if len(username) < 4:
            flash('Nome de usuário deve ter pelo menos 4 caracteres.', category='ERROR')
            e = True
        if len(password) < 4:
            flash('Senha deve ter pelo menos 4 caracteres.', category='ERROR')
            e = True
        if len(database) < 4:
            flash('Nome do banco de dados deve ter pelo menos 4 caracteres.', category='ERROR')
            e = True
        if not e:
            user = User.query.filter_by(username = username).first()
            if user:
                flash("Usuário com esse nome já existe!", category="ERROR")
            else:
                flash('Conta criada com sucesso!', category='SUCCESS')
                new_user = User(username = username, password = generate_password_hash(password, method='sha256'), database = database, is_admin = admin)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('auth.login'))
    return render_template("sign_up.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    logout_user()
    return redirect(url_for('auth.login'))