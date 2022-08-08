from unicodedata import category
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .mypokeAPI import *
import sys
sys.path.append("..")

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
            print (species)
            print (retorna_especie(species))
            if retorna_especie(species):
                incluir_pokemon(name+","+cost+","+species+","+trn_id)
            else:
                flash("A espécie de nome " + species + " não foi encontrada, favor inserir o nome de uma espécie válida", category="ERROR")
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            if query_category == 'Nome':
                db = [selecionar_pokemon(query_text)]
            elif query_category == 'Valor Mensal':
                db = retorna_pokemons_do_custo_mensal(query_text)
            elif query_category == 'Tipo':
                db = retorna_pokemons_do_tipo(query_text)
            elif query_category == 'Espécie':
                db = retorna_pokemons_da_especie(query_text)
            elif query_category == 'Nome de Treinador':
                db = retorna_pokemons_de_pessoa_nome_treinador(query_text)
            elif query_category == 'ID de Treinador':
                db = retorna_pokemons_de_pessoa_id_treinador(query_text)
            return render_template("pokemon/pokemon_add.html", user=current_user, db=db)
        
    db = retorna_tabela_pokemons()
    return render_template("pokemon/pokemon_add.html", user=current_user, db=db)

@views.route('/pkmn/srch', methods=['GET', 'POST'])
def pokemon_srch():
    if request.method == 'POST':
        query_category = request.form.get('query-category')
        query_text = request.form.get('query-text')
        print(query_category+"----------->"+query_text)
        if query_category == 'Nome':
            db = selecionar_pokemon(query_text)
        elif query_category == 'Valor Mensal':
            db = retorna_pokemons_do_custo_mensal(query_text)
        elif query_category == 'Tipo':
            db = retorna_pokemons_do_tipo(query_text)
        elif query_category == 'Espécie':
            db = retorna_pokemons_da_especie(query_text)
        elif query_category == 'Nome de Treinador':
            db = retorna_pokemons_de_pessoa_nome_treinador(query_text)
        elif query_category == 'ID de Treinador':
            db = retorna_pokemons_de_pessoa_id_treinador(query_text)
        return render_template("pokemon/pokemon_query.html", user=current_user, db=db)
            
    db = retorna_tabela_pokemons()
    return render_template("pokemon/pokemon_query.html", user=current_user, db=db)
    

@views.route('/pkmn/del', methods=['GET', 'POST'])
def pokemon_del():
    if request.method == 'POST':
        if request.form.get('query-category') == None:
            remove_name = request.form.get('remove-name')
            excluir_pokemon(remove_name)
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            if query_category == 'Nome':
                db = [selecionar_pokemon(query_text)]
            elif query_category == 'Valor Mensal':
                db = retorna_pokemons_do_custo_mensal(query_text)
            elif query_category == 'Tipo':
                db = retorna_pokemons_do_tipo(query_text)
            elif query_category == 'Espécie':
                db = retorna_pokemons_da_especie(query_text)
            elif query_category == 'Nome de Treinador':
                db = retorna_pokemons_de_pessoa_nome_treinador(query_text)
            elif query_category == 'ID de Treinador':
                db = retorna_pokemons_de_pessoa_id_treinador(query_text)
            return render_template("pokemon/pokemon_remove.html", user=current_user, db=db)
        
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
                old_data = selecionar_pokemon(name).pop()
                if (trn_id == ''):
                    trn_id = old_data[6]
                if (species == ''):
                    species = old_data[2]
                if (cost == ''):
                    cost = old_data[3]
                atualizar_pokemon(name, cost, species, trn_id)
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            if query_category == 'Nome':
                db = [selecionar_pokemon(query_text)]
            elif query_category == 'Valor Mensal':
                db = retorna_pokemons_do_custo_mensal(query_text)
            elif query_category == 'Tipo':
                db = retorna_pokemons_do_tipo(query_text)
            elif query_category == 'Espécie':
                db = retorna_pokemons_da_especie(query_text)
            elif query_category == 'Nome de Treinador':
                db = retorna_pokemons_de_pessoa_nome_treinador(query_text)
            elif query_category == 'ID de Treinador':
                db = retorna_pokemons_de_pessoa_id_treinador(query_text)
            return render_template("pokemon/pokemon_update.html", user=current_user, db=db)
        
    db = retorna_tabela_pokemons()
    return render_template("pokemon/pokemon_update.html", user=current_user, db=db)

@views.route('/trn/add', methods=['GET', 'POST'])
def trainer_add():
    if request.method == 'POST':
        if request.form.get('query-category') == None:
            # Add
            name = request.form.get('add-name')
            trn_id = request.form.get('add-id')
            birthday = converte_birthday(request.form.get('add-date'))
            
            incluir_pessoa(name+","+trn_id+","+birthday)
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            if query_category == 'Nome':
                db = selecionar_pessoas_nome(query_text)
            elif query_category == 'ID de Treinador':
                db = selecionar_pessoa(query_text)
            elif query_category == 'Data de Nascimento':
                db = selecionar_pessoas_data_nasc(query_text)

            return render_template("trainer/trainer_add.html", user=current_user, db=db)            
        
    db = retorna_tabela_pessoas()
    return render_template("trainer/trainer_add.html", user=current_user, db=db)

@views.route('/trn/<int:trn_id>', methods=['GET', 'POST'])
def trn_id(trn_id):
    db = retorna_pokemons_de_pessoa_id_treinador (trn_id)
    treinador = retorna_treinador (trn_id)
    return render_template("trainer/trainer_home.html", user=current_user, db=db, treinador=treinador)

@views.route('/trn/srch', methods=['GET', 'POST'])
def trainer_srch():
    if request.method == 'POST':
        # Query
        query_category = request.form.get('query-category')
        query_text = request.form.get('query-text')
        if query_category == 'Nome':
            db = selecionar_pessoas_nome(query_text)
        elif query_category == 'ID de Treinador':
            db = selecionar_pessoa(query_text)
        elif query_category == 'Data de Nascimento':
            db = selecionar_pessoas_data_nasc(query_text)
        
        return render_template("trainer/trainer_query.html", user=current_user, db=db) 
    
    db = retorna_tabela_pessoas()
    return render_template("trainer/trainer_query.html", user=current_user, db=db)

@views.route('/trn/del', methods=['GET', 'POST'])
def trainer_del():
    if request.method == 'POST':
        if request.form.get('query-category') == None:
            remove_id = request.form.get('remove-id')
            excluir_pessoa(remove_id)
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            if query_category == 'Nome':
                db = selecionar_pessoas_nome(query_text)
            elif query_category == 'ID de Treinador':
                db = selecionar_pessoa(query_text)
            elif query_category == 'Data de Nascimento':
                db = selecionar_pessoas_data_nasc(query_text)
            
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
                birthday = converte_birthday(request.form.get('upd-date'))
                old_data = selecionar_pessoa(trn_id).pop()
                print(old_data)
                if name == "":
                    name = old_data[0]
                if birthday == "":
                    birthday = old_data[2]
                atualizar_pessoa(trn_id, name, birthday)            
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            if query_category == 'Nome':
                db = selecionar_pessoas_nome(query_text)
            elif query_category == 'ID de Treinador':
                db = selecionar_pessoa(query_text)
            elif query_category == 'Data de Nascimento':
                db = selecionar_pessoas_data_nasc(query_text)
            
            return render_template("trainer/trainer_update.html", user=current_user, db=db)
    
    db = retorna_tabela_pessoas()
    return render_template("trainer/trainer_update.html", user=current_user, db=db)

def converte_birthday(old_birthday):
    print(old_birthday)
    b = old_birthday.split("-")
    print(b)
    b.reverse()
    print(b)
    birthday = ""
    for u in b:
        birthday += u
        birthday += "/"
    birthday = birthday[:-1]
    return birthday