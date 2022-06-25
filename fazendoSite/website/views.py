from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/home')
def home():
    return render_template("landing.html", user_name="User")

@views.route('/pokemon/add')
def pokemon_add():
    return render_template("pokemon_add.html", user_name="User")