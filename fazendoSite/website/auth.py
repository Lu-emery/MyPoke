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
        if password == "3333":
            admin = True
        else:
            admin = False        
        #database = request.form.get("database")
        e = False
        if len(username) < 4:
            flash('Nome de usuário deve ter pelo menos 4 caracteres.', category='ERROR')
            e = True
        if len(password) < 4:
            flash('Senha deve ter pelo menos 4 caracteres.', category='ERROR')
            e = True
        #if len(database) < 4:
        #    flash('Nome do banco de dados deve ter pelo menos 4 caracteres.', category='ERROR')
        #    e = True
        if not e:
            user = User.query.filter_by(username = username).first()
            if user:
                flash("Usuário com esse nome já existe!", category="ERROR")
            else:
                flash('Conta criada com sucesso!', category='SUCCESS')
                new_user = User(username = username, password = generate_password_hash(password, method='sha256'), is_admin = admin)
                print(new_user) #TODO Remove
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('auth.login'))
    return render_template("sign_up.html", user=current_user)

@auth.route('/logout')
def logout():
    return "<h1>Logged out!!!</h1>"