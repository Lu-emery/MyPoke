#####################################################################
# myPokeAPI.py - API de manutenção do banco de dados myPoké
# Versão: 0.8
#
# Contribuidores: Lucas Emery
#                 Thiago Damasceno
#
# Funcionalidade:
#    Esse arquivo contém as funções do CRUD do banco de dados myPoké
#    a partir dele, consegue-se criar, remover, editar e deletar entidades
#    das classes Pessoa e Pokémon.
#####################################################################
#
# Changelog:
#   0.1: Teste de conexão com o postgresql usando psycopg2
#   0.2: Implementação das funções de inserção e remoção de pessoa e pokémon
#   0.2.1: Documentação do arquivo e funções existentes e adequação ao pep8
#   0.3: Implementação das funções de deleção e reinicialização de tabelas
#   0.4: Implementação da função de atualização de pessoa
#   0.4.1: Documentação das funções adicionadas, changelog e lista todo
#   0.7.0: Implementação das funções de consulta
#   0.7.1: Implementação de Querries avançadas
#   0.8.0 Implementação da tabela "Espécies"
#
#####################################################################
#
# TODO:
#   Tratamento de erros
#       Inserção de instâncias com as mesmas chaves primárias
#   
#   Teste de funcionalidade
#       Deleção, reinicialização
#       Atualização de pessoa
#
#   Adição de funcionalidade
#       Funções de busca (pessoa e pokémon)
#       Atualização de pokémon
#
#####################################################################

USER='postgres'
PASSWORD='admin'
HOST='localhost'
PORT='5432'

# psycopg2: ferramenta utilizada para fazer a ponte entre posgresql e python
from pydoc import doc
import psycopg2

def criar_base_de_dados():
    connection = psycopg2.connect(database ='postgres', user=USER, password=PASSWORD, host=HOST, port=PORT)#(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute ('CREATE DATABASE mypoke;')
    print('Base de dados mypoke criada com sucesso!')
    # Completa e commita o processo de remoção
    connection.commit()
    criar_tabela_pessoas()
    criar_tabela_especies()
    criar_tabela_pokemons()
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

def deletar_base_de_dados():
    connection = psycopg2.connect(database = 'postgres', user=USER, password=PASSWORD, host=HOST, port= PORT)
    connection.autocommit = True
    cursor = connection.cursor()

    deletar_tabela_pessoas()
    deletar_tabela_especies()
    deletar_tabela_pokemons()
    connection.commit()

    cursor.execute ('DROP DATABASE mypoke;')
    print('Base de dados mypoke excluída com sucesso!')
    # Completa e commita o processo de remoção
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

def reiniciar_base_de_dados():
    deletar_base_de_dados()
    criar_base_de_dados()


# criar_tabela_pessoas()
#   Cria uma tabela vazia de pessoas
#   Entrada: nenhuma
#   Saída: nenhuma
def criar_tabela_pessoas():

    # Acessa o banco de dados

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando CREATE do postgresql, caso a tabela pessoas ainda não exista
    #   define os parâmetros de pessoa como 'nome, id_treinador, data_nascimento'
    cursor.execute ("""CREATE TABLE IF NOT EXISTS pessoas (
                        nome_treinador VARCHAR,
                        id_treinador BIGINT PRIMARY KEY,
                        data_nascimento VARCHAR);""")
    # Finaliza e comita a criação de tabela
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    
# criar_tabela_pokemons()
#   Cria uma tabela vazia de pokemons
#   Entrada: nenhuma
#   Saída: nenhuma
def criar_tabela_pokemons():

    # Acessa o banco de dados

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando CREATE do postgresql, caso a tabela pokemons ainda não exista
    #   define os parâmetros de pokemon como 'nome, custo_mensal, especie,
    #                                         tipo_primario, tipo_secundario,
    #                                         id_treinador'
    cursor.execute ("""CREATE TABLE IF NOT EXISTS pokemons (
                        id_pokemon SERIAL PRIMARY KEY,
                        nome_pokemon VARCHAR,
                        custo_mensal DOUBLE PRECISION,
                        especie VARCHAR,
                        id_treinador BIGINT REFERENCES pessoas (id_treinador));""")
    # Finaliza e comita a criação de tabela
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

def criar_tabela_especies():


    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("""CREATE TABLE IF NOT EXISTS especies (
                        especie VARCHAR PRIMARY KEY,
                        tipo_primario VARCHAR,
                        tipo_secundario VARCHAR);""")
    connection.commit()

    cursor.close()
    connection.close()
    
# deletar_tabela_pessoas()
#   Deleta a tabela de pessoas e a tabela de pokémons associada
#       isso se dá porque a existência de uma tabela de pokémons
#       requer uma tabela de treinadores
#   Entrada: nenhuma
#   Saída: nenhuma
def deletar_tabela_pessoas():

    # Acessa o banco de dados

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando DROP TABLE para ambas as tabelas, caso existam
    cursor.execute ("""DROP TABLE IF EXISTS pessoas CASCADE;""")
    # Finaliza e comita a deleção das tabelas
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

def deletar_tabela_especies():

    # Acessa o banco de dados

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando DROP TABLE para a tabela espécies, caso exista
    cursor.execute ("""DROP TABLE IF EXISTS especie CASCADE;""")
    # Finaliza e comita a deleção da tabela
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# deletar_tabela_pokémons()
#   Deleta a tabela de pokémons
#       isso pode ser feito sem a deleção da tabela de pessoas
#   Entrada: nenhuma
#   Saída: nenhuma  
def deletar_tabela_pokemons():

    # Acessa o banco de dados

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando DROP TABLE para a tabela pokemons, caso exista
    cursor.execute ("""DROP TABLE IF EXISTS pokemons;""")
    # Finaliza e comita a deleção da tabela
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# reiniciar_tabela(nome_tabela)
#   Reinicia ambas as tabelas caso o argumento seja 'pessoas'
#            e só a tabela pokémon caso o argumento seja 'pokemons'
#   Entrada: uma string 'nome_tabela' que deve ser 'pessoas' ou 'pokemons'
#   Saída: nenhuma   
def reiniciar_tabela(nome_tabela):

    if (nome_tabela == 'pessoas'):
        # Caso o argumento seja 'pessoas,' deleta ambas as tabelas
        #   pelo comando deletar_tabela_pessoas() e então
        #   cria ambas as tabelas vazias novamente
        deletar_tabela_pokemons()
        deletar_tabela_pessoas()
        criar_tabela_pessoas()
        criar_tabela_pokemons()
    
    elif (nome_tabela == 'pokemons'):
        # Caso o argumento seja 'pokemons,' deleta somente a tabela pokemons
        #   e então cria a tabela vazia novamente
        deletar_tabela_pokemons()
        criar_tabela_pokemons()
    
    else:
        # Caso o usuário insira um argumento inválido, uma mensagem de erro é exibida
        return 'Tabela com nome ' + str(nome_tabela) + ' não encontrada, favor fornecer o nome de uma tabela existente'
    

def incluir_especie(entrada):
    
    # Acessa o banco de dados

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Divide a string de entrada nos parâmetros referentes aos campos da tabela e armazena em 'valores'
    especie, tipo_primario, tipo_secundario = (entrada.replace(';', '')).split(',')
    if (tipo_secundario == ''):
        tipo_secundario = 'NULL'
    valores = "'" + especie + "'" + ", " + "'" + tipo_primario + "'" + ", " + "'" + tipo_secundario + "'"

    cursor.execute ("""INSERT INTO especies (especie, tipo_primario, tipo_secundario) 
                    VALUES ("""+ valores + ");")
    # Completa e commita o processo de inserção
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    
# incluir_pessoa(informacoes)
#   Insere uma pessoa nova no banco de dados
#   Entrada: uma string no formato "nome,id_treinador,data_nascimento"
#   Saída: nenhuma
def incluir_pessoa(entrada):

    # Acessa o banco de dados

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Divide a string de entrada nos parâmetros referentes aos campos da tabela e armazena em 'valores'
    nome, id_treinador, data_nascimento = (entrada.replace(';', '')).split(',')
    valores = "'" + nome + "'" + ", " + "'" + str (id_treinador) + "'" + ", " + "'" + data_nascimento + "'"

    # Executa o comando INSERT em postgresql para inserir a instância na tabela
    cursor.execute ("""INSERT INTO pessoas (nome_treinador, id_treinador, data_nascimento)
                     VALUES ("""+ valores + ");")
    # Completa e commita o processo de inserção
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# incluir_pokemon(informacoes)
#   Insere um pokemon novo no banco de dados
#   Entrada: uma string no formato "nome,custo_mensal,especie,tipo_primario,tipo_secundario,id_treinador_dono"
#   Saída: nenhuma
def incluir_pokemon(entrada):
    
    # Acessa o banco de dados

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Divide a string de entrada nos parâmetros referentes aos campos da tabela e armazena em 'valores'
    nome, custo_mensal, especie, id_treinador = (entrada.replace(';', '')).split(',')
    valores = "'" + nome + "'" + ", " + "'" + str (custo_mensal) + "'" + ", " + "'" + especie + "'" + ", " + "'" + str (id_treinador) + "'"

    # Executa o comando INSERT em postgresql para inserir a instância na tabela
    cursor.execute ("""INSERT INTO pokemons (nome_pokemon, custo_mensal, especie, id_treinador) 
                    VALUES ("""+ valores + ");")
    # Completa e commita o processo de inserção
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    
def atualizar_pessoa(id_treinador, nome, data_nascimento):

    # Acessa o banco de dados

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Determina se o usuário quer fazer a alteração do nome, data de nascimento ou ambos
    #   então, executa o comando UPDATE pessoas SET [] para alterar as colunas em questão
    #   na linha onde 'id_treinador' é igual ao argumento passado
    cursor.execute (""" UPDATE pessoas
                        SET nome_treinador = """ + "'" + nome + "'" + ", data_nascimento = " + "'" + data_nascimento + "'" +
                        " WHERE id_treinador = " + "'" + str(id_treinador) + "'" + ";")
    # Completa e commita o processo de alteração da tabela
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

def atualizar_pokemon(nome_pokemon, custo_mensal, especie, id_treinador):


    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute (""" UPDATE pokemons
                        SET custo_mensal = """ + "'" + str(custo_mensal) + "'" + 
                        ", especie = " + "'" + especie + "'" +
                        ", id_treinador = " + "'" + str(id_treinador) + "'" +
                        " WHERE nome_pokemon = " + "'" + nome_pokemon + "'" + ";")
    connection.commit()

    cursor.close()
    connection.close()

def selecionar_pessoa(id_treinador):


    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("""SELECT * FROM pessoas
                       WHERE id_treinador = """ + str (id_treinador) + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry.pop()

def selecionar_pokemon(nome):


    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("""SELECT * FROM pokemons
                       WHERE nome_pokemon = """ + "'" + nome + "';")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry.pop()


def retorna_tabela_pessoas():


    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("SELECT * FROM pessoas")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry

def retorna_tabela_pokemons():


    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("""SELECT id_pokemon,
                        nome_pokemon,
                        custo_mensal,
                        especie,
                        tipo_primario,
                        COALESCE (tipo_secundario, ' '),
                        id_treinador 
                        FROM pokemons NATURAL JOIN especies""")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    print (resultado_querry)
    return resultado_querry

def retorna_tabela_especies():


    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("SELECT * FROM especies")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry

def retorna_pokemons_de_pessoa_id_treinador(id_treinador):


    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("""SELECT * FROM pokemons
                       WHERE id_treinador = """ + str(id_treinador) + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry

def retorna_pokemons_do_tipo(tipo):


    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("""SELECT * FROM pokemons NATURAL JOIN especies
                       WHERE tipo_primario = """ + "'" + tipo + "'" + " OR tipo_secundario = " + "'" + tipo + "'" + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry

def retorna_pokemons_da_especie(especie):


    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("""SELECT * FROM pokemons
                       WHERE especie = """ + "'" + especie + "'" + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry

# excluir_pessoa(id_treinador)
#   Exclui a pessoa com a chave primaria 'id_treinador'
#   Entrada: uma string que contém o número de id_treinador da pessoa a ser excluida
#   Saída: nenhuma
def excluir_pessoa(id_treinador):
    
    # Acessa o banco de dados

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando DELETE em postgresql para remover a instância na tabela com a chave primária 'id_treinador' igual ao argumento
    cursor.execute ("DELETE FROM pokemons WHERE id_treinador = " + "'" + str (id_treinador) + "'" + ";")
    cursor.execute ("DELETE FROM pessoas WHERE id_treinador = " + "'" + str (id_treinador) + "'" + ";")
    # Completa e commita o processo de remoção
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# excluir_pokemon(nome_pokemon)
#   Exclui o pokémon com a chave primaria 'nome_pokemon'
#   Entrada: uma string que contém o nome do pokémon a ser excluido
#   Saída: nenhuma
def excluir_pokemon(nome_pokemon):
    
    # Acessa o banco de dados

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando DELETE em postgresql para remover a instância na tabela com a chave primária 'nome_pokemon' igual ao argumento
    cursor.execute ("DELETE FROM pokemons WHERE nome = " + "'" + nome_pokemon + "'" + ";")
    # Completa e commita o processo de remoção
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

def excluir_especie(especie):

    # Acessa o banco de dados

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("DELETE FROM especies WHERE especie = " + "'" + especie + "'" + ";")
    # Completa e commita o processo de inserção
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# QUERRIES AVANÇADAS

def retorna_tipos_especie(especie):

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("""SELECT tipo primario, tipo secundario FROM especies
                       WHERE especie = """ + "'" + especie + "'" + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry

def retorna_propietarios_de_especie(especie):

    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("""SELECT nome_treinador, id_treinador FROM pessoas NATURAL JOIN pokemons
                       WHERE especie = """ + "'" + especie + "'" + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry

def retorna_pokemons_de_pessoa_nome_treinador(nome_treinador):


    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("""SELECT nome_pokemon, custo_mensal, especie, tipo_primario, tipo_secundario FROM pokemons NATURAL JOIN pessoas
                       WHERE nome_treinador = """ + "'" + nome_treinador + "'" + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry

def retorna_treinadores_com_custo_maior(custo_mensal):


    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    cursor.execute ("""WITH custo_por_treinador AS (
	                SELECT SUM (custo_mensal) AS custo_total, id_treinador 
                    FROM pokemons
                    GROUP BY id_treinador)
                    SELECT nome_treinador, id_treinador, data_nascimento 
                    FROM pessoas NATURAL JOIN custo_por_treinador
                    WHERE pessoas.id_treinador = custo_por_treinador.id_treinador 
                    AND custo_total > """ + str(custo_mensal) + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry


#################################################################################
# COMANDOS DE TESTE
# TODO: REMOVER

def popular_bd():
    #deletar_base_de_dados()
    incluir_especie('Charizard,Fogo,Voador')
    incluir_especie('Dragonite,Dragao,')
    incluir_especie('Jolteon,Eletrico,')
    incluir_especie('Butterfree,Inseto,Voador')
    incluir_especie('Ghastly,Fantasma,')
    incluir_especie('Zapdos,Voador,Elétrico')
    incluir_pessoa ('Rafa,555551278,21/03/1999;')
    incluir_pessoa ('Lucas,665551278,16/06/1998;')
    incluir_pessoa ('Carlinhos,555555555,23/05/1994;')
    incluir_pokemon('Mayu,150.00,Charizard,665551278;')
    incluir_pokemon('Viny,200.00,Dragonite,665551278;')
    incluir_pokemon('Sparky,80.00,Jolteon,555555555;')
    incluir_pokemon('Charla,150.00,Charizard,555551278;')
    incluir_pokemon('Aurora,65.50,Butterfree,555551278;')
    incluir_pokemon('Ghastly,100.50,Ghastly,555551278;')
    incluir_pokemon('Rafa Zapdos,600,Zapdos,555551278;')
    #excluir_pokemon ("Charla")
    #excluir_pessoa (555551278)
    #atualizar_pessoa(555551278,'Rafa','24/03/1999')
    #reiniciar_tabela('pessoas')
    #print (retorna_tabela_pokemons())
    #print (selecionar_pessoa(555551278))
    #print (retorna_pokemons_de_pessoa_id_treinador(555551278))
    #pokemons_voadores = retorna_pokemons_do_tipo('Voador')
    #pokemons_voadores.sort(key=lambda x:x[1])
    #print (pokemons_voadores)
    #excluir_pessoa (555551278)
    #print (retorna_tabela_pokemons())
    #print (retorna_tabela_pessoas())
    #print (retorna_propietarios_de_especie('Charizard'))
    #print (retorna_pokemons_de_pessoa_nome_treinador('Rafa'))
    #print (retorna_treinadores_com_custo_maior(900))
    #print (retorna_tabela_especies())
    #deletar_base_de_dados()
    return
