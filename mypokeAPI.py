import psycopg2
from databaseconfig import config

def inserirPessoa(nome, documento, data_nascimento):

    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    cursor.execute ("INSERT INTO pessoas (nome, documento, data_nascimento) VALUES (" + nome + ", " + documento + ", " + data_nascimento + ");")
    connection.commit()

    cursor.close()
    connection.close()
