from unicodedata import category
from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", user_name="Login")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
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
            flash('Conta criada com sucesso!', category='SUCCESS')
            pass
    return render_template("sign_up.html")

@auth.route('/logout')
def logout():
    return "<h1>Logged out!!!</h1>"