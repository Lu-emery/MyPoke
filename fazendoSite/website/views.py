from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

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
            species = request.form.get('add-species')
            prim_type = request.form.get('add-type-prim')
            sec_type = request.form.get('add-type-sec')
            if sec_type == "":
                sec_type = None
            print([name, species, prim_type, sec_type, trn_id])
            #TODO fazer o add
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            print([query_category, query_text])
            #TODO fazer a query
    return render_template("pokemon/pokemon_add.html", user=current_user)

@views.route('/pkmn/srch', methods=['GET', 'POST'])
def pokemon_srch():
    if request.method == 'POST':
        query_category = request.form.get('query-category')
        query_text = request.form.get('query-text')
        print([query_category, query_text])
        #TODO fazer a query
    return render_template("pokemon/pokemon_query.html", user=current_user)

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
            print([query_category, query_text])
            #TODO fazer a query
    return render_template("pokemon/pokemon_remove.html", user=current_user)

@views.route('/pkmn/upd', methods=['GET', 'POST'])
def pokemon_upd():
    if request.method == 'POST':
        if request.form.get('query-category') == None:
            # Upd
            name = request.form.get('upd-name')
            trn_id = request.form.get('upd-id')
            species = request.form.get('upd-species')
            prim_type = request.form.get('upd-type-prim')
            sec_type = request.form.get('upd-type-sec')
            data = [name, species, prim_type, sec_type, trn_id]
            for count, elem in enumerate(data):
                if elem == "":
                    data[count] = None
            print(data)
            #TODO fazer o Update
        else:
            # Query
            query_category = request.form.get('query-category')
            query_text = request.form.get('query-text')
            print([query_category, query_text])
            #TODO fazer a query
    return render_template("pokemon/pokemon_update.html", user=current_user)

@views.route('/trn/add', methods=['GET', 'POST'])
def trainer_add():
    if request.form.get('query-category') == None:
        # Add
        name = request.form.get('add-name')
        trn_id = request.form.get('add-id')
        birthday = request.form.get('add-date')
        print([name, trn_id, birthday])
        #TODO fazer o add
    else:
        # Query
        query_category = request.form.get('query-category')
        query_text = request.form.get('query-text')
        print([query_category, query_text])
        #TODO fazer a query
    return render_template("trainer/trainer_add.html", user=current_user)

@views.route('/trn/srch', methods=['GET', 'POST'])
def trainer_srch():
    # Query
    query_category = request.form.get('query-category')
    query_text = request.form.get('query-text')
    print([query_category, query_text])
    #TODO fazer a query
    return render_template("trainer/trainer_query.html", user=current_user)

@views.route('/trn/del', methods=['GET', 'POST'])
def trainer_del():
    if request.form.get('query-category') == None:
        # Del
        pass
        #TODO fazer o add
    else:
        # Query
        query_category = request.form.get('query-category')
        query_text = request.form.get('query-text')
        print([query_category, query_text])
        #TODO fazer a query
    return render_template("trainer/trainer_remove.html", user=current_user)

@views.route('/trn/upd', methods=['GET', 'POST'])
def trainer_upd():
    if request.form.get('query-category') == None:
        # Upd
        name = request.form.get('upd-name')
        trn_id = request.form.get('upd-id')
        birthday = request.form.get('upd-date')
        data = [name, trn_id, birthday]
        for count, elem in enumerate(data):
            if elem == "":
                data[count] = None
        print(data)
        #TODO fazer o Update
    else:
        # Query
        query_category = request.form.get('query-category')
        query_text = request.form.get('query-text')
        print([query_category, query_text])
        #TODO fazer a query
    return render_template("trainer/trainer_update.html", user=current_user)