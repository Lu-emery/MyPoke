from unicodedata import category
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .mypokeAPI import *
import sys
sys.path.append("..")


#import psycopg2
#USER='postgres'
#PASSWORD='senha'
#HOST='127.0.0.1'
#PORT='5432'

views = Blueprint('views', __name__)

@views.route('/home')
@login_required
def home():
    return render_template("landing.html", user=current_user)

@views.route('/help')
def help():
    return render_template("help.html", user=current_user)

@views.route('/pkmn/add', methods=['GET', 'POST'])
def pokemon_add():
    if request.method == 'POST':
        if request.form.get('query-category') == None:
            # Add
            name = request.form.get('add-name')
            trn_id = request.form.get('add-id')
            cost = request.form.get('add-cost')
            species = request.form.get('add-species')
            prim_type = request.form.get('add-type-prim')
            sec_type = request.form.get('add-type-sec')
            incluir_pokemon(name+","+cost+","+species+","+trn_id)
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            if query_category == 'Nome':
                db = selecionar_pokemon(query_text)
            elif query_category == 'Valor Mensal':
                db = retorna_pokemons_do_valor_mensal(query_text)
            elif query_category == 'Tipo':
                db = retorna_pokemons_do_tipo(query_text)
            elif query_category == 'Espécie':
                db = retorna_pokemons_da_especie(query_text)
            elif query_category == 'ID de Treinador':
                db = retorna_pokemons_de_pessoa_id_treinador(query_text)
            return render_template("pokemon/pokemon_query.html", user=current_user, db=db)
        
    db = retorna_tabela_pokemons()
    return render_template("pokemon/pokemon_add.html", user=current_user, db=db)

@views.route('/pkmn/srch', methods=['GET', 'POST'])
def pokemon_srch():
    if request.method == 'POST':
        query_category = request.form.get('query-category')
        query_text = request.form.get('query-text')
        if query_category == 'Nome':
<<<<<<< HEAD
            db = selecionar_pokemon (query_text)
=======
            db = selecionar_pokemon(query_text)
>>>>>>> 469c1fb6be7ecb5c9940d7abd6bc17df61612d59
        elif query_category == 'Valor Mensal':
            db = retorna_pokemons_do_valor_mensal(query_text)
        elif query_category == 'Tipo':
            db = retorna_pokemons_do_tipo(query_text)
        elif query_category == 'Espécie':
            db = retorna_pokemons_da_especie(query_text)
        elif query_category == 'ID de Treinador':
            db = retorna_pokemons_de_pessoa_id_treinador(query_text)
        return render_template("pokemon/pokemon_query.html", user=current_user, db=db)
            
    db = retorna_tabela_pokemons()
    return render_template("pokemon/pokemon_query.html", user=current_user, db=db)
    

@views.route('/pkmn/del', methods=['GET', 'POST'])
def pokemon_del():
    if request.method == 'POST':
        if request.form.get('query-category') == None:
            # Del
            pass
            #TODO fazer o delete
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            if query_category == 'Nome':
                db = selecionar_pokemon(query_text)
            elif query_category == 'Valor Mensal':
                db = retorna_pokemons_do_valor_mensal(query_text)
            elif query_category == 'Tipo':
                db = retorna_pokemons_do_tipo(query_text)
            elif query_category == 'Espécie':
                db = retorna_pokemons_da_especie(query_text)
            elif query_category == 'ID de Treinador':
                db = retorna_pokemons_de_pessoa_id_treinador(query_text)
            return render_template("pokemon/pokemon_query.html", user=current_user, db=db)
        
    db = retorna_tabela_pokemons()
    return render_template("pokemon/pokemon_remove.html", user=current_user, db=db)

@views.route('/pkmn/upd', methods=['GET', 'POST'])
def pokemon_upd():
    if request.method == 'POST':
        if request.form.get('query-category') == None:
            # Upd
            name = request.form.get('upd-name')
            if name == "":
                flash("Por favor insira o nome do pokémon a ser atualizado.", category="ERROR")
            else:
                trn_id = request.form.get('upd-id')
                species = request.form.get('upd-species')
                cost = request.form.get('upd-cost')
                prim_type = request.form.get('upd-type-prim')
                sec_type = request.form.get('upd-type-sec')
                data = [cost, species, trn_id]
                old_data = selecionar_pokemon(name)
                for count, elem in enumerate(data):
                    if elem == "":
                        data[count] = str(old_data[count+2])
                atualizar_pokemon(name, data[0], data[1], data[2])
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            if query_category == 'Nome':
                db = selecionar_pokemon(query_text)
            elif query_category == 'Valor Mensal':
                db = retorna_pokemons_do_valor_mensal(query_text)
            elif query_category == 'Tipo':
                db = retorna_pokemons_do_tipo(query_text)
            elif query_category == 'Espécie':
                db = retorna_pokemons_da_especie(query_text)
            elif query_category == 'ID de Treinador':
                db = retorna_pokemons_de_pessoa_id_treinador(query_text)
            return render_template("pokemon/pokemon_query.html", user=current_user, db=db)
        
    db = retorna_tabela_pokemons()
    return render_template("pokemon/pokemon_update.html", user=current_user, db=db)

@views.route('/trn/add', methods=['GET', 'POST'])
def trainer_add():
    if request.method == 'POST':
        if request.form.get('query-category') == None:
            # Add
            name = request.form.get('add-name')
            trn_id = request.form.get('add-id')
            birthday = request.form.get('add-date')
            
            print(birthday)
            
            incluir_pessoa(name+","+trn_id+","+birthday)
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            if query_category == 'Nome':
                #TODO
                pass
            elif query_category == 'ID de Treinador':
                #TODO
                pass
            elif query_category == 'Data de Nascimento':
                #TODO
                pass

            db = retorna_tabela_pessoas()##
            return render_template("trainer/trainer_add.html", user=current_user, db=db)            
        
    db = retorna_tabela_pessoas()
    return render_template("trainer/trainer_add.html", user=current_user, db=db)

@views.route('/trn/srch', methods=['GET', 'POST'])
def trainer_srch():
    if request.method == 'POST':
        # Query
        query_category = request.form.get('query-category')
        query_text = request.form.get('query-text')
        if query_category == 'Nome':
            #TODO
            pass
        elif query_category == 'ID de Treinador':
            #TODO
            pass
        elif query_category == 'Data de Nascimento':
            #TODO
            pass
        
        db = retorna_tabela_pessoas()##
        return render_template("trainer/trainer_query.html", user=current_user, db=db) 
    
    db = retorna_tabela_pessoas()
    return render_template("trainer/trainer_query.html", user=current_user, db=db)

@views.route('/trn/del', methods=['GET', 'POST'])
def trainer_del():
    if request.method == 'POST':
        if request.form.get('query-category') == None:
            # Del
            pass
            #TODO fazer o add
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            if query_category == 'Nome':
                #TODO
                pass
            elif query_category == 'ID de Treinador':
                #TODO
                pass
            elif query_category == 'Data de Nascimento':
                #TODO
                pass
            
            db = retorna_tabela_pessoas()##
            return render_template("trainer/trainer_remove.html", user=current_user, db=db)
        
    db = retorna_tabela_pessoas()
    return render_template("trainer/trainer_remove.html", user=current_user, db=db)

@views.route('/trn/upd', methods=['GET', 'POST'])
def trainer_upd():
    if request.method == 'POST':
        if request.form.get('query-category') == None:
            # Upd
            trn_id = request.form.get('upd-id')
            if trn_id == "":
                flash("Por favor insira o ID do treinador a ser atualizado.", category="ERROR")
            else:
                name = request.form.get('upd-name')
                birthday = request.form.get('upd-date')
                data = [name, birthday]
                old_data = selecionar_pessoa(trn_id)
                for count, elem in enumerate(data):
                    if elem == "":
                        data[count] = old_data[count+1]
                atualizar_pessoa(trn_id, data[0], data[1])            
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            if query_category == 'Nome':
                #TODO
                pass
            elif query_category == 'ID de Treinador':
                #TODO
                pass
            elif query_category == 'Data de Nascimento':
                #TODO
                pass
            
            db = retorna_tabela_pessoas()
            return render_template("trainer/trainer_update.html", user=current_user, db=db)

    
    db = retorna_tabela_pessoas()
    return render_template("trainer/trainer_update.html", user=current_user, db=db)