import psycopg2
from databaseconfig import config

def inserirPessoa(nome, documento, data_nascimento):

    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    valores = "'" + nome + "'" + ", " + "'" + str (documento) + "'" + ", " + "'" + data_nascimento + "'"

    cursor.execute ("""INSERT INTO pessoas (nome, documento, data_nascimento)
                     VALUES ("""+ valores + ");")
    connection.commit()

    cursor.close()
    connection.close()

def inserirPokemon(nome, custo_mensal, tipo_primario, tipo_secundario, documento_dono, especie):

    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    valores = "'" + nome + "'" + ", " + "'" + str (custo_mensal) + "'" + ", " + "'" + tipo_primario + "'" + ", " + "'" + tipo_secundario + "'" + ", " + "'" + str (documento_dono) + "'" + ", " + "'" + especie + "'"

    cursor.execute ("""INSERT INTO pokemons (nome, custo_mensal, tipo_primario, tipo_secundario, documento_dono, especie) 
                    VALUES ("""+ valores + ");")
    connection.commit()

    cursor.close()
    connection.close()

def excluirPessoa(documento):

    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    cursor.execute ("DELETE FROM pessoas WHERE documento = " + "'" + str (documento) + "'" + ";")
    connection.commit()

    cursor.close()
    connection.close()

def excluirPokemon(nome):

    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    cursor.execute ("DELETE FROM pokemons WHERE nome = " + "'" + nome + "'" + ";")
    connection.commit()

    cursor.close()
    connection.close()

#inserirPokemon("Charla", 150.00, 'Fogo', 'Voador', 555551234, 'Charizard')
#inserirPessoa ("Rafa", 555551278, '21/03/1999')
excluirPokemon ("Charla")
excluirPessoa (555551278)