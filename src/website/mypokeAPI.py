#####################################################################
# myPokeAPI.py - API de manutenção do banco de dados myPoké
# Versão: 1.1.1
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
#   0.8.1 Hotfix nas funções de retorno de tabela
#   1.0 Finalização da implementação das funções
#   1.1 Atualização das funções para o novo formato de visualização no front-end
#   1.1.1 Documentação final
#
#####################################################################

# Dados usados para o acesso inicial ao sistema, para criar o banco de dados no postgres
USER='postgres'
PASSWORD='admin'
HOST='localhost'
PORT='5432'

# psycopg2: ferramenta utilizada para fazer a ponte entre posgresql e python
from pydoc import doc
import psycopg2

# criar_base_de_dados()
#   cria a base de dados mypoke e as suas respectivas tabelas
def criar_base_de_dados():
    connection = psycopg2.connect(database ='postgres', user=USER, password=PASSWORD, host=HOST, port=PORT)#(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    connection.autocommit = True
    cursor = connection.cursor()

    # Cria a base de dados mypoke
    cursor.execute ('CREATE DATABASE mypoke;')
    print('Base de dados mypoke criada com sucesso!')
    connection.commit()
    
    # Cria as tabelas internas
    criar_tabela_pessoas()
    criar_tabela_especies()
    criar_tabela_pokemons()
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# deletar_base_de_dados()
#   deleta a base de dados mypoke e as suas respectivas tabelas
def deletar_base_de_dados():
    connection = psycopg2.connect(database = 'postgres', user=USER, password=PASSWORD, host=HOST, port= PORT)
    connection.autocommit = True
    cursor = connection.cursor()

    # Deleta as tabelas internas
    deletar_tabela_pessoas()
    deletar_tabela_especies()
    deletar_tabela_pokemons()
    connection.commit()

    # Deleta a base de dados
    cursor.execute ('DROP DATABASE mypoke;')    
    print('Base de dados mypoke excluída com sucesso!')
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    
# inicializar_mypoke()
#   cria a base de dados, contém alguns comandos de teste
def inicializar_mypoke():
    connection = psycopg2.connect(database = 'postgres', user=USER, password=PASSWORD, host=HOST, port= PORT)
    connection.autocommit = True
    cursor = connection.cursor()
    
    # Verifica se o banco de dados já existe
    cursor.execute('SELECT datname FROM pg_database')
    list_db = cursor.fetchall()
    connection.commit()
    
    if ('mypoke',) in list_db:
        # comando de teste
        # deletar_base_de_dados()
        pass
    else:
        # Caso não exista, cria o banco de dados no postgres e popula a tabela espécies
        criar_base_de_dados()
        pokedex()
    
    # comando de teste
    # Popula o banco de dados com os dados de exemplo
    popular_bd()
    
    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()


# criar_tabela_pessoas()
#   cria uma tabela vazia de pessoas
def criar_tabela_pessoas():
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando CREATE do postgresql, caso a tabela pessoas ainda não exista
    #   define os parâmetros de pessoa como 'nome, id_treinador, data_nascimento'
    cursor.execute ("""CREATE TABLE IF NOT EXISTS pessoas (
                        nome_treinador VARCHAR,
                        id_treinador VARCHAR PRIMARY KEY,
                        data_nascimento VARCHAR);""")
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    
# criar_tabela_pokémons()
#   cria uma tabela vazia de pokémons
def criar_tabela_pokemons():
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando CREATE do postgresql, caso a tabela pokémons ainda não exista
    #   define os parâmetros de pokémon como 'nome, especie, custo_mensal, id_treinador'
    cursor.execute ("""CREATE TABLE IF NOT EXISTS pokemons (
                        id_pokemon SERIAL PRIMARY KEY,
                        nome_pokemon VARCHAR,
                        especie VARCHAR,
                        custo_mensal DOUBLE PRECISION,
                        id_treinador VARCHAR REFERENCES pessoas (id_treinador));""")
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# criar_tabela_especies()
#   cria uma tabela vazia de espécies
def criar_tabela_especies():
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando CREATE do postgresql, caso a tabela de espécies ainda não exista
    #   define os parâmetros de espécie como 'espécie, tipo_primario, tipo_secundario'
    cursor.execute ("""CREATE TABLE IF NOT EXISTS especies (
                        especie VARCHAR PRIMARY KEY,
                        tipo_primario VARCHAR,
                        tipo_secundario VARCHAR);""")
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    
# deletar_tabela_pessoas()
#   deleta a tabela de pessoas e a tabela de pokémons associada
#       isso se dá porque a existência de uma tabela de pokémons
#       requer uma tabela de treinadores
def deletar_tabela_pessoas():
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando DROP TABLE para ambas as tabelas, caso existam
    cursor.execute ("""DROP TABLE IF EXISTS pessoas CASCADE;""")
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# deletar_tabela_especies()
#   deleta a tabela de espécies
def deletar_tabela_especies():
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando DROP TABLE para a tabela espécies, caso exista
    cursor.execute ("""DROP TABLE IF EXISTS especie CASCADE;""")
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# deletar_tabela_pokémons()
#   Deleta a tabela de pokémons
def deletar_tabela_pokemons():
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando DROP TABLE para a tabela pokémons, caso exista
    cursor.execute ("""DROP TABLE IF EXISTS pokemons;""")
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# reiniciar_tabela(nome_tabela)
#   reinicia ambas as tabelas caso o argumento seja 'pessoas'
#            e só a tabela pokémon caso o argumento seja 'pokémons'
#   Entrada: uma string 'nome_tabela' que deve ser 'pessoas' ou 'pokémons'
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
        # Caso o argumento seja 'pokémons,' deleta somente a tabela pokémons
        #   e então cria a tabela vazia novamente
        deletar_tabela_pokemons()
        criar_tabela_pokemons()
    
    else:
        # Caso o usuário insira um argumento inválido, uma mensagem de erro é exibida
        return 'Tabela com nome ' + str(nome_tabela) + ' não encontrada, favor fornecer o nome de uma tabela existente'
    
# incluir_especie(entrada)
#   adiciona uma nova espécie na tabela de espécies
#   Entrada: uma string 'espécie,tipo_primario,tipo_secundario;'
#               a string 'tipo_secundario' pode ser vazia
def incluir_especie(entrada):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Divide a string de entrada nos parâmetros referentes aos campos da tabela e armazena em 'valores'
    especie, tipo_primario, tipo_secundario = (entrada.replace(';', '')).split(',')
    valores = "'" + especie + "'" + ", " + "'" + tipo_primario + "'" + ", " + "'" + tipo_secundario + "'"

    # Faz a correção de nomes de espécies com caracteres especiais
    especie = corrige_nome(especie)

    # Insere a espécie na tabela    
    cursor.execute ("""INSERT INTO especies (especie, tipo_primario, tipo_secundario) 
                    VALUES ("""+ valores + ");")
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    
# incluir_pessoa(dados)
#   adiciona uma pessoa nova no banco de dados
#   Entrada: uma string no formato "nome,id_treinador,data_nascimento"
def incluir_pessoa(entrada):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Divide a string de entrada nos parâmetros referentes aos campos da tabela e armazena em 'valores'
    nome, id_treinador, data_nascimento = (entrada.replace(';', '')).split(',')
    valores = "'" + nome + "'" + ", " + "'" + str (id_treinador) + "'" + ", " + "'" + data_nascimento + "'"

    # Insere o treinador na tabela
    cursor.execute ("""INSERT INTO pessoas (nome_treinador, id_treinador, data_nascimento)
                     VALUES ("""+ valores + ");")
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# incluir_pokemon(entrada)
#   adiciona um pokémon novo no banco de dados
#   Entrada: uma string no formato "nome,custo_mensal,especie,id_treinador"
def incluir_pokemon(entrada):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Divide a string de entrada nos parâmetros referentes aos campos da tabela e armazena em 'valores'
    nome, custo_mensal, especie, id_treinador = (entrada.replace(';', '')).split(',')
    valores = "'" + nome + "'" + ", " + "'" + str (custo_mensal) + "'" + ", " + "'" + especie + "'" + ", " + "'" + str (id_treinador) + "'"

    # Faz a correção de nomes de espécies com caracteres especiais
    especie = corrige_nome(especie)
    
    # Insere o pokémon na tabela
    cursor.execute ("""INSERT INTO pokemons (nome_pokemon, custo_mensal, especie, id_treinador) 
                    VALUES ("""+ valores + ");")
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    
# atualizar_pessoa(id_treinador, nome, data_nascimento)
#   atualiza o treinador de id 'id_treinador' com um ou mais dados alterados
#   Entrada: strings 'id_treinador', 'nome' e 'data_nascimento'
#               os dados 'nome' e 'data_nascimento' que não serão alterados terão o valor antigo
def atualizar_pessoa(id_treinador, nome, data_nascimento):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Executa o comando UPDATE pessoas SET [] para alterar a data de nascimento e o nome
    #   do treinador cujo 'id_treinador' é igual ao argumento passado
    cursor.execute (""" UPDATE pessoas
                        SET nome_treinador = """ + "'" + nome + "'" + ", data_nascimento = " + "'" + data_nascimento + "'" +
                        " WHERE id_treinador = " + "'" + str(id_treinador) + "'" + ";")
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# atualizar_pokemon(nome_pokemon, custo_mensal, especie, id_treinador)
#   atualiza o pokémon de nome 'nome_pokemon' com um ou mais dados alterados
#   Entrada: strings 'nome_pokemon', 'custo_mensal', 'especie', e 'id_treinador'
#               os dados 'custo_mensal', 'especie' e 'id_treinador' que não serão alterados terão o valor antigo
def atualizar_pokemon(nome_pokemon, custo_mensal, especie, id_treinador):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Faz a correção de nomes de espécies com caracteres especiais
    especie = corrige_nome(especie)

    # Executa o comando UPDATE pokemons SET [] para alterar os dados
    #   do pokémon cujo 'nome_pokemon' é igual ao argumento passado
    cursor.execute (""" UPDATE pokemons
                        SET custo_mensal = """ + "'" + str(custo_mensal) + "'" + 
                        ", especie = " + "'" + especie + "'" +
                        ", id_treinador = " + "'" + str(id_treinador) + "'" +
                        " WHERE nome_pokemon = " + "'" + nome_pokemon + "'" + ";")
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# selecionar_pessoa(id_treinador)
#   seleciona o treinador com ID igual ao argumento
#   Entrada: string 'id_treinador'
#   Saída: lista de treinadores com um elemento
def selecionar_pessoa(id_treinador):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Seleciona os treinadores cujo 'id_treinador' é igual ao argumento passado
    #   por ser uma chave primária, sempre retorna um único treinador
    cursor.execute ("""SELECT * FROM pessoas
                       WHERE id_treinador = """ + "'" + str (id_treinador) + "';")
    resultado_querry = cursor.fetchall()
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    return resultado_querry

# selecionar_pokemon(nome)
#   seleciona o pokémon com nome igual ao argumento
#   Entrada: string 'nome'
#   Saída: lista de pokémons com um elemento
def selecionar_pokemon(nome):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Seleciona os pokémons cujo 'nome_pokemon' é igual ao argumento passado
    #   por ser uma chave primária, sempre retorna um único pokémon
    cursor.execute ("""SELECT id_pokemon,
                        nome_pokemon,
                        especie,
                        custo_mensal,
                        tipo_primario,
                        tipo_secundario,
                        nome_treinador,
                        id_treinador 
                        FROM pokemons NATURAL JOIN especies NATURAL JOIN pessoas
                        WHERE nome_pokemon = """ + "'" + nome + "';")
    resultado_querry = cursor.fetchall()
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    return resultado_querry

# selecionar_pessoas_nome(nome)
#   seleciona os treinadores com nome igual ao argumento
#   Entrada: string 'nome'
#   Saída: lista de treinadores
def selecionar_pessoas_nome(nome):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Seleciona os treinadores cujo 'nome_treinador' é igual ao argumento passado
    cursor.execute ("""SELECT nome_treinador,
                        id_treinador,
                        data_nascimento
                        FROM pessoas
                        WHERE nome_treinador = """ + "'" + nome + "';")
    resultado_querry = cursor.fetchall()
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    return resultado_querry

# selecionar_pessoas_data_nasc(data_nascimento)
#   seleciona os treinadores com data de nascimento igual ao argumento
#   Entrada: string 'data_nascimento'
#   Saída: lista de treinadores
def selecionar_pessoas_data_nasc(data_nascimento):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Seleciona os treinadores cuja 'data_nascimento' é igual ao argumento passado
    cursor.execute ("""SELECT nome_treinador,
                        id_treinador,
                        data_nascimento
                        FROM pessoas
                        WHERE data_nascimento = """ + "'" + data_nascimento + "';")
    resultado_querry = cursor.fetchall()
    connection.commit()


    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    return resultado_querry

# retorna_tabela_pessoas()
#   retorna a tabela completa de treinadores
#   Saída: lista de treinadores
def retorna_tabela_pessoas():
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Seleciona todos os treinadores
    cursor.execute ("SELECT * FROM pessoas")
    resultado_querry = cursor.fetchall()
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    return resultado_querry

# retorna_tabela_pokemons()
#   retorna a tabela completa de pokémons
#   Saída: lista de pokémons
def retorna_tabela_pokemons():
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Seleciona todos os pokémons
    cursor.execute ("""SELECT id_pokemon,
                        nome_pokemon,
                        especie,
                        custo_mensal,
                        tipo_primario,
                        tipo_secundario,
                        nome_treinador,
                        id_treinador 
                        FROM pokemons NATURAL JOIN especies NATURAL JOIN pessoas""")
    resultado_querry = cursor.fetchall()
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    return resultado_querry

# retorna_tabela_especies()
#   retorna a tabela completa de espécies
#   Saída: lista de espécies
def retorna_tabela_especies():
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Seleciona todas as espécies
    cursor.execute ("SELECT * FROM especies")
    resultado_querry = cursor.fetchall()
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    return resultado_querry

# retorna_pokemons_de_pessoa_id_treinador(id_treinador)
#   retorna todos os pokémons que o treinador identificado pelo argumento tem
#   Entrada: string 'id_treinador'
#   Saída: lista de pokémons
def retorna_pokemons_de_pessoa_id_treinador(id_treinador):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Seleciona todos os pokémons que tem como chave estrangeira o argumento
    cursor.execute ("""SELECT id_pokemon,
                        nome_pokemon,
                        especie,
                        custo_mensal,
                        tipo_primario,
                        tipo_secundario,
                        nome_treinador,
                        id_treinador 
                        FROM pokemons NATURAL JOIN especies NATURAL JOIN pessoas
                       WHERE id_treinador = """ + "'" + str(id_treinador) + "'" + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    return resultado_querry

# retorna_pokemons_do_tipo(tipo)
#   retorna todos os pokémons com um dos tipos igual ao argumento
#   Entrada: string 'tipo'
#   Saída: lista de pokémons
def retorna_pokemons_do_tipo(tipo):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Seleciona todos os pokémons cujo 'tipo_primario' ou 'tipo_secundário' é igual ao argumento
    cursor.execute ("""SELECT id_pokemon,
                        nome_pokemon,
                        especie,
                        custo_mensal,
                        tipo_primario,
                        tipo_secundario,
                        nome_treinador,
                        id_treinador 
                        FROM pokemons NATURAL JOIN especies NATURAL JOIN pessoas
                       WHERE tipo_primario = """ + "'" + tipo + "'" + " OR tipo_secundario = " + "'" + tipo + "'" + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    return resultado_querry

# retorna_pokemons_do_custo_mensal(custo_mensal)
#   retorna todos os pokemons com custo mensal igual ao argumento
#   Entrada: string 'custo_mensal'
#   Saída: lista de pokémons
def retorna_pokemons_do_custo_mensal(custo_mensal):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Seleciona todos os pokémons com 'custo_mensal' igual ao argumento
    cursor.execute ("""SELECT id_pokemon,
                        nome_pokemon,
                        especie,
                        custo_mensal,
                        tipo_primario,
                        tipo_secundario,
                        nome_treinador,
                        id_treinador 
                        FROM pokemons NATURAL JOIN especies NATURAL JOIN pessoas
                        WHERE custo_mensal = """ + "'" + custo_mensal + "';")
    resultado_querry = cursor.fetchall()
    connection.commit()

    # Encerra a conexão com o banco de dados    
    cursor.close()
    connection.close()
    return resultado_querry

# retorna_pokemons_da_especie(especie)
#   retorna todos os pokémons com espécie igual ao argumento
#   Entrada: string 'especie'
#   Saída: lista de pokémons
def retorna_pokemons_da_especie(especie):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Faz a correção de nomes de espécies com caracteres especiais
    especie = corrige_nome(especie)

    # Seleciona todos os pokémons cuja 'especie' é igual ao argumento
    cursor.execute ("""SELECT id_pokemon,
                        nome_pokemon,
                        especie,
                        custo_mensal,
                        tipo_primario,
                        tipo_secundario,
                        nome_treinador,
                        id_treinador 
                        FROM pokemons NATURAL JOIN especies NATURAL JOIN pessoas
                       WHERE especie = """ + "'" + especie + "'" + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    # Encerra a conexão com o banco de dados    
    cursor.close()
    connection.close()
    return resultado_querry

# excluir_pessoa(id_treinador)
#   exclui o treinador com a chave primaria 'id_treinador' e todos os pokémons vinculados a esse treinador
#   Entrada: string 'id_treinador'
def excluir_pessoa(id_treinador):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Deleta todos os pokémons cuja chave estrangeira é igual ao argumento
    #   então, deleta todos os treinadores cujo 'id_treinador' é igual ao argumento
    #   por ser uma chave primária, só exclui um treinador
    cursor.execute ("DELETE FROM pokemons WHERE id_treinador = " + "'" + str (id_treinador) + "'" + ";")
    cursor.execute ("DELETE FROM pessoas WHERE id_treinador = " + "'" + str (id_treinador) + "'" + ";")
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# excluir_pokemon(nome_pokemon)
#   exclui o pokémon com a chave primaria 'nome_pokemon'
#   Entrada: string 'nome_pokemon'
def excluir_pokemon(nome_pokemon):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Deleta todos os pokémons cujo 'nome_pokemon' é igual ao argumento
    #   por ser uma chave primária, só exclui um pokemon
    cursor.execute ("DELETE FROM pokemons WHERE nome_pokemon = " + "'" + nome_pokemon + "'" + ";")
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# retorna_pokemons_de_pessoa_nome_treinador(nome_treinador)
#   retorna todos os pokémons de treinadores com o nome 'nome_treinador'
#       por não ser uma chave primária, pode retornar pokémons de mais de um treinador
#   Entrada: string 'nome_treinador'
#   Saída: lista de pokémons
def retorna_pokemons_de_pessoa_nome_treinador(nome_treinador):
    connection = psycopg2.connect(database = 'mypoke', user=USER, password=PASSWORD, host=HOST, port= PORT)
    cursor = connection.cursor()

    # Seleciona todos os pokémons de todos os treinadores cujo nome é igual ao argumento
    cursor.execute ("""SELECT id_pokemon,
                        nome_pokemon,
                        especie,
                        custo_mensal,
                        tipo_primario,
                        tipo_secundario,
                        nome_treinador,
                        id_treinador 
                        FROM pokemons NATURAL JOIN especies NATURAL JOIN pessoas
                       WHERE nome_treinador = """ + "'" + nome_treinador + "'" + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    return resultado_querry

# corrige_nome(especie)
#   corrige e sanitiza nomes de espécies com caracteres especiais, para a forma que o banco de dados usa eles
#   Entrada: string 'especie'
#   Saída: string
def corrige_nome(especie):
    # Apóstrofos causam erros no psycopg2, então o banco de dados remove ele
    if especie == "Farfetch'd":
        return "Farfetchd"
    # Usuários podem escrever Mr Mime sem o ponto, logo, colocamos ele de volta
    if especie == "Mr Mime":
        return "Mr. Mime"
    
    # A maior parte dos usuários não terá as teclas ♂ e ♀, logo, damos uma alternativa de como escrever
    if especie == "Nidoran(m)" or especie == "Nidoran (m)":
        return "Nidoran♂"
    if especie == "Nidoran(f)" or especie == "Nidoran (f)":
        return "Nidoran♀"

    # Nenhum outro nome de pokémon causa erros
    else:
        return especie

# pokedex()
#   insere no banco de dados todas as 151 espécies da primeira geração e seus respectivos tipos
#       usamos a tipagem mais recente dos pokémons, ao invés da tipagem original deles na primeira geração
def pokedex():
    incluir_especie('Bulbasaur,Grama,Venenoso')
    incluir_especie('Ivysaur,Grama,Venenoso')
    incluir_especie('Venusaur,Grama,Venenoso')
    incluir_especie('Charmander,Fogo,')
    incluir_especie('Charmeleon,Fogo,')
    incluir_especie('Charizard,Fogo,Voador')
    incluir_especie('Squirtle,Água,')
    incluir_especie('Wartortle,Água,')
    incluir_especie('Blastoise,Água,')
    incluir_especie('Caterpie,Inseto,')
    incluir_especie('Metapod,Inseto,')
    incluir_especie('Butterfree,Inseto,Voador')
    incluir_especie('Weedle,Inseto,Venenoso')
    incluir_especie('Kakuna,Inseto,Venenoso')
    incluir_especie('Beedrill,Inseto,Venenoso')
    incluir_especie('Pidgey,Normal,Voador')
    incluir_especie('Pidgeotto,Normal,Voador')
    incluir_especie('Pidgeot,Normal,Voador')
    incluir_especie('Rattata,Normal,')
    incluir_especie('Raticate,Normal,')
    incluir_especie('Spearow,Normal,Voador')
    incluir_especie('Fearow,Normal,Voador')
    incluir_especie('Ekans,Venenoso,')
    incluir_especie('Arbok,Venenoso,')
    incluir_especie('Pikachu,Elétrico,')
    incluir_especie('Raichu,Elétrico,')
    incluir_especie('Sandshrew,Terra,')
    incluir_especie('Sandslash,Terra,')
    incluir_especie('Nidoran♀,Venenoso,')
    incluir_especie('Nidorina,Venenoso,')
    incluir_especie('Nidoqueen,Venenoso,Terra')
    incluir_especie('Nidoran♂,Venenoso,')
    incluir_especie('Nidorino,Venenoso,')
    incluir_especie('Nidoking,Venenoso,Terra')
    incluir_especie('Clefairy,Fada,')
    incluir_especie('Clefable,Fada,')
    incluir_especie('Vulpix,Fogo,')
    incluir_especie('Ninetales,Fogo,')
    incluir_especie('Jigglypuff,Normal,Fada')
    incluir_especie('Wigglytuff,Normal,Fada')
    incluir_especie('Zubat,Venenoso,Voador')
    incluir_especie('Golbat,Venenoso,Voador')
    incluir_especie('Oddish,Grama,Venenoso')
    incluir_especie('Gloom,Grama,Venenoso')
    incluir_especie('Vileplume,Grama,Venenoso')
    incluir_especie('Paras,Inseto,Grama')
    incluir_especie('Parasect,Inseto,Grama')
    incluir_especie('Venonat,Venenoso,Inseto')
    incluir_especie('Venomoth,Venenoso,Inseto')
    incluir_especie('Diglett,Terra,')
    incluir_especie('Dugtrio,Terra,')
    incluir_especie('Meowth,Normal,')
    incluir_especie('Persian,Normal,')
    incluir_especie('Psyduck,Água,')
    incluir_especie('Golduck,Água,')
    incluir_especie('Mankey,Lutador,')
    incluir_especie('Primeape,Lutador,')
    incluir_especie('Growlithe,Fogo,')
    incluir_especie('Arcanine,Fogo,')
    incluir_especie('Poliwag,Água,')
    incluir_especie('Poliwhirl,Água,')
    incluir_especie('Poliwrath,Água,Lutador')
    incluir_especie('Abra,Psíquico,')
    incluir_especie('Kadabra,Psíquico,')
    incluir_especie('Alakazam,Psíquico,')
    incluir_especie('Machop,Lutador,')
    incluir_especie('Machoke,Lutador,')
    incluir_especie('Machamp,Lutador,')
    incluir_especie('Bellsprout,Grama,Venenoso')
    incluir_especie('Weepinbell,Grama,Venenoso')
    incluir_especie('Victreebel,Grama,Venenoso')
    incluir_especie('Tentacool,Água,Venenoso')
    incluir_especie('Tentacruel,Água,Venenoso')
    incluir_especie('Geodude,Pedra,Terra')
    incluir_especie('Graveler,Pedra,Terra')
    incluir_especie('Golem,Pedra,Terra')
    incluir_especie('Ponyta,Fogo,')
    incluir_especie('Rapidash,Fogo,')
    incluir_especie('Slowpoke,Água,Psíquico')
    incluir_especie('Slowbro,Água,Psíquico')
    incluir_especie('Magnemite,Elétrico,Metálico')
    incluir_especie('Magneton,Elétrico,Metálico')
    incluir_especie('Farfetchd,Normal,Voador')
    incluir_especie('Doduo,Normal,Voador')
    incluir_especie('Dodrio,Normal,Voador')
    incluir_especie('Seel,Água,')
    incluir_especie('Dewgong,Água,Gelo')
    incluir_especie('Grimer,Venenoso,')
    incluir_especie('Muk,Venenoso,')
    incluir_especie('Shellder,Água,')
    incluir_especie('Cloyster,Água,Gelo')
    incluir_especie('Gastly,Fantasma,Venenoso')
    incluir_especie('Haunter,Fantasma,Venenoso')
    incluir_especie('Gengar,Fantasma,Venenoso')
    incluir_especie('Onix,Pedra,Terra')
    incluir_especie('Drowzee,Psíquico,')
    incluir_especie('Hypno,Psíquico,')
    incluir_especie('Krabby,Água,')
    incluir_especie('Kingler,Água,')
    incluir_especie('Voltorb,Elétrico,')
    incluir_especie('Electrode,Elétrico,')
    incluir_especie('Exeggcute,Grama,Psíquico')
    incluir_especie('Exeggutor,Grama,Psíquico')
    incluir_especie('Cubone,Terra,')
    incluir_especie('Marowak,Terra,')
    incluir_especie('Hitmonlee,Lutador,')
    incluir_especie('Hitmonchan,Lutador,')
    incluir_especie('Lickitung,Normal,')
    incluir_especie('Koffing,Venenoso,')
    incluir_especie('Weezing,Venenoso,')
    incluir_especie('Rhyhorn,Terra,Pedra')
    incluir_especie('Rhydon,Terra,Pedra')
    incluir_especie('Chansey,Normal,')
    incluir_especie('Tangela,Grama,')
    incluir_especie('Kangaskhan,Normal,')
    incluir_especie('Horsea,Água,')
    incluir_especie('Seadra,Água,')
    incluir_especie('Goldeen,Água,')
    incluir_especie('Seaking,Água,')
    incluir_especie('Staryu,Água,')
    incluir_especie('Starmie,Água,Psíquico')
    incluir_especie('Mr. Mime,Psíquico,Fada')
    incluir_especie('Scyther,Inseto,Voador')
    incluir_especie('Jynx,Gelo,Psíquico')
    incluir_especie('Electabuzz,Elétrico,')
    incluir_especie('Magmar,Fogo,')
    incluir_especie('Pinsir,Inseto,')
    incluir_especie('Tauros,Normal,')
    incluir_especie('Magikarp,Água,')
    incluir_especie('Gyarados,Água,Voador')
    incluir_especie('Lapras,Água,Gelo')
    incluir_especie('Ditto,Normal,')
    incluir_especie('Eevee,Normal,')
    incluir_especie('Vaporeon,Água,')
    incluir_especie('Jolteon,Elétrico,')
    incluir_especie('Flareon,Fogo,')
    incluir_especie('Porygon,Normal,')
    incluir_especie('Omanyte,Pedra,Água')
    incluir_especie('Omastar,Pedra,Água')
    incluir_especie('Kabuto,Pedra,Água')
    incluir_especie('Kabutops,Pedra,Água')
    incluir_especie('Aerodactyl,Pedra,Voador')
    incluir_especie('Snorlax,Normal,')
    incluir_especie('Articuno,Gelo,Voador')
    incluir_especie('Zapdos,Elétrico,Voador')
    incluir_especie('Moltres,Fogo,Voador')
    incluir_especie('Dratini,Dragão,')
    incluir_especie('Dragonair,Dragão,')
    incluir_especie('Dragonite,Dragão,Voador')
    incluir_especie('Mewtwo,Psíquico,')
    incluir_especie('Mew,Psíquico,')

# função de teste
# popular_bd()
#   preenche o banco de dados com alguns exemplos para facilitar a visualização e testes
def popular_bd():

    incluir_pessoa ('Lucas,665551278,16/06/1998;')

    incluir_pokemon('Mayu,150.00,Charizard,665551278;')
    incluir_pokemon('Viny,200.00,Dragonite,665551278;')
    

    incluir_pessoa ('Carlinhos,555555555,23/05/1994;')

    incluir_pokemon('Sparky,80.00,Jolteon,555555555;')
    

    incluir_pessoa ('Rafa,555551278,21/03/1999;')

    incluir_pokemon('Charla,150.00,Charizard,555551278;')
    incluir_pokemon('Aurora,65.50,Butterfree,555551278;')
    incluir_pokemon('Ghastly,100.50,Gastly,555551278;')
    incluir_pokemon('RafaZapdos,600,Zapdos,555551278;')