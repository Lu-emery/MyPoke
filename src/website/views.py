from unicodedata import category
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .mypokeAPI import *
import matplotlib.pyplot as plt
import numpy as np
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
            errored = False
            if not name or not trn_id or not cost or not species:
                errored = True
                flash("Para adicionar um pokémon, favor preencher todos os campos.", category="ERROR")
            if not retorna_especie(species):
                errored = True
                flash("A espécie de nome " + species + " não foi encontrada, favor inserir o nome de uma espécie válida", category="ERROR")
            if not retorna_treinador(trn_id):
                errored = True
                flash("Favor inserir um ID de treinador válido", category="ERROR")
            for c in name:
                if c in (" ", "'", '"'):
                    errored = True
                    flash("Nomes de pokémons não podem conter espaços ou aspas, favor inserir um nome válido", category="ERROR")
            if not errored:
                incluir_pokemon(name+","+cost+","+species+","+trn_id)
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
    db = None
    if request.method == 'POST':
        if request.form.get('remove-name') != None:
            # Del
            remove_name = request.form.get('remove-name')
            excluir_pokemon(remove_name)
        elif request.form.get('upd-name') or request.form.get('upd-id') or request.form.get('upd-cost') or request.form.get('upd-species'):
            # Upd
            name = request.form.get('upd-name')
            trn_id = request.form.get('upd-id')
            species = request.form.get('upd-species')
            cost = request.form.get('upd-cost')
            errored = False
            if species and not retorna_especie(species):
                errored = True
                flash("A espécie de nome " + species + " não foi encontrada, favor inserir o nome de uma espécie válida", category="ERROR")
            if trn_id and not retorna_treinador(trn_id):
                errored = True
                flash("Favor inserir um ID de treinador válido", category="ERROR")
            for c in name:
                if c in (" ", "'", '"'):
                    errored = True
                    flash("Nomes de pokémons não podem conter espaços ou aspas, favor inserir um nome válido", category="ERROR")
            if not errored:
                old_data = selecionar_pokemon(name).pop()
                if (trn_id == ''):
                    trn_id = old_data[7]
                if (species == ''):
                    species = old_data[2]
                if (cost == ''):
                    cost = old_data[3]
                atualizar_pokemon(name, cost, species, trn_id)
        else:
            # Srch
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
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

    if not db:
        db = retorna_tabela_pokemons()
        
    cria_graficos(db)
    
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
            trn_id = request.form.get('upd-id')
            species = request.form.get('upd-species')
            cost = request.form.get('upd-cost')
            errored = False
            if species and not retorna_especie(species):
                errored = True
                flash("A espécie de nome " + species + " não foi encontrada, favor inserir o nome de uma espécie válida", category="ERROR")
            if trn_id and not retorna_treinador(trn_id):
                errored = True
                flash("Favor inserir um ID de treinador válido", category="ERROR")
            if not errored:        
                old_data = selecionar_pokemon(name).pop()
                if (trn_id == ''):
                    trn_id = old_data[7]
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
            errored = False
            if not name or not trn_id or not birthday:
                errored = True
                flash("Para adicionar um treinador, favor preencher todos os campos.", category="ERROR")
            if trn_id[0] == "0":
                errored = True
                flash("O primeiro caracter do ID do treinador não pode ser 0.", category="ERROR")
            if selecionar_pessoa(trn_id):
                errored = True
                flash("IDs de treinador devem ser únicos, e esse já está sendo usado.", category="ERROR")
            for c in name:
                if c in (" ", "'", '"'):
                    errored = True
                    flash("Nomes de treinadores não podem conter espaços ou aspas, favor inserir um nome válido", category="ERROR")
            if not errored:
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
    db = None
    if request.method == 'POST':
        if request.form.get('add-name'):
            # Add
            name = request.form.get('add-name')
            trn_id = request.form.get('add-id')
            cost = request.form.get('add-cost')
            species = request.form.get('add-species')
            errored = False
            if not name or not trn_id or not cost or not species:
                errored = True
                flash("Para adicionar um pokémon, favor preencher todos os campos.", category="ERROR")
            if species and not retorna_especie(species):
                errored = True
                flash("A espécie de nome " + species + " não foi encontrada, favor inserir o nome de uma espécie válida", category="ERROR")
            for c in name:
                if c in (" ", "'", '"'):
                    errored = True
                    flash("Nomes de pokémons não podem conter espaços ou aspas, favor inserir um nome válido", category="ERROR")
            if not errored:
                incluir_pokemon(name+","+cost+","+species+","+trn_id)
        elif request.form.get('remove-name'):
            # Del
            remove_name = request.form.get('remove-name')
            excluir_pokemon(remove_name)
        elif request.form.get('upd-name') or request.form.get('upd-id') or request.form.get('upd-cost') or request.form.get('upd-species'):
            # Upd
            name = request.form.get('upd-name')
            trn_id = request.form.get('upd-id')
            species = request.form.get('upd-species')
            cost = request.form.get('upd-cost')
            errored = False
            if species and not retorna_especie(species):
                errored = True
                flash("A espécie de nome " + species + " não foi encontrada, favor inserir o nome de uma espécie válida", category="ERROR")
            if trn_id and not retorna_treinador(trn_id):
                errored = True
                flash("Favor inserir um ID de treinador válido", category="ERROR")
            for c in name:
                if c in (" ", "'", '"'):
                    errored = True
                    flash("Nomes de pokémons não podem conter espaços ou aspas, favor inserir um nome válido", category="ERROR")
            if not errored:
                old_data = selecionar_pokemon(name).pop()
                if (trn_id == ''):
                    trn_id = old_data[7]
                if (species == ''):
                    species = old_data[2]
                if (cost == ''):
                    cost = old_data[3]
                atualizar_pokemon(name, cost, species, trn_id)
        else:
            # Srch
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
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
        
    if not db:
        db = retorna_pokemons_de_pessoa_id_treinador (trn_id)
    treinador = retorna_treinador (trn_id)
    
    cria_graficos(db)
    
    return render_template("trainer/trainer_home.html", user=current_user, db=db, treinador=treinador)


@views.route('/trn/srch', methods=['GET', 'POST'])
def trainer_srch():
    if request.method == 'POST':
        if request.form.get('remove-id') != None:
            # Del
            remove_id = request.form.get('remove-id')
            excluir_pessoa(remove_id)
        elif request.form.get('upd-id'):
            # Upd
            trn_id = request.form.get('upd-id')
            name = request.form.get('upd-name')
            birthday = converte_birthday(request.form.get('upd-date'))
            errored = False
            for c in name:
                if c in (" ", "'", '"'):
                    errored = True
                    flash("Nomes de treinadores não podem conter espaços ou aspas, favor inserir um nome válido", category="ERROR")
            if not errored:    
                old_data = selecionar_pessoa(trn_id).pop()
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
            name = request.form.get('upd-name')
            birthday = converte_birthday(request.form.get('upd-date'))
            errored = False
            for c in name:
                if c in (" ", "'", '"'):
                    errored = True
                    flash("Nomes de treinadores não podem conter espaços ou aspas, favor inserir um nome válido", category="ERROR")
            if not errored:        
                old_data = selecionar_pessoa(trn_id).pop()
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
    b = old_birthday.split("-")
    b.reverse()
    birthday = ""
    for u in b:
        birthday += u
        birthday += "/"
    birthday = birthday[:-1]
    return birthday

def cria_graficos(db):
    especies = {"keys": [],"values": []}
    tipos = {"keys": [],"values": []}
    
    for pokemon in db:
        
        species = pokemon[2]
        prim_type = pokemon[4]
        sec_type = None
        if pokemon[5] != "":
            sec_type = pokemon[5]
            
        if species in especies['keys']:
            i = especies['keys'].index(species)
            especies['values'][i] += 1
        else:
            especies['keys'].append(species)
            especies['values'].append(1)
            
        if prim_type in tipos['keys']:
            i = tipos['keys'].index(prim_type)
            tipos['values'][i] += 1
        else:
            tipos['keys'].append(prim_type)
            tipos['values'].append(1)
            
        if sec_type:
            if sec_type in tipos['keys']:
                i = tipos['keys'].index(sec_type)
                tipos['values'][i] += 1
            else:
                tipos['keys'].append(sec_type)
                tipos['values'].append(1)
    
    especies['keys'] = [x for _, x in sorted(zip(especies['values'], especies['keys']), key=lambda pair: pair[0])]
    especies['values'] = sorted(especies['values'])
    tipos['keys'] = [x for _, x in sorted(zip(tipos['values'], tipos['keys']), key=lambda pair: pair[0])]
    tipos['values'] = sorted(tipos['values'])

    species_colors = plt.get_cmap('cool')(np.linspace(0.2, 0.7, len(especies['keys'])))
    
    fig1, ax1 = plt.subplots()
    ax1.pie(np.array(especies['values']), labels=np.array(especies['keys']), colors = species_colors, autopct=make_autopct_especie(especies['values']), startangle=90)
    fig1.savefig("website/static/species_graph.png")
    
    fig2, ax2 = plt.subplots()
    ax2.pie(np.array(tipos['values']), labels=np.array(tipos['keys']), colors = species_colors, autopct = make_autopct_tipos(tipos['values'], len(db)), startangle=90)
    fig2.savefig("website/static/types_graph.png")
    
def make_autopct_especie(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        if total > 5:
            if val == 1:
                return f'({val})'
        return f'{pct:.2f}%  ({val})'
    return my_autopct
    
def make_autopct_tipos(values, size):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        pct = val/size*100
        if total > 5:
            if val == 1:
                return f'({val})'
        return f'{pct:.2f}%  ({val})'
    return my_autopct
