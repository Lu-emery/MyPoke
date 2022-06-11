#####################################################################
# myPokeAPI.py - API de manutenção do banco de dados myPoké
# Versão: 0.7
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


# psycopg2: ferramenta utilizada para fazer a ponte entre posgresql e python
from pydoc import doc
import psycopg2
from databaseconfig import config

def criar_base_de_dados():
    connection = psycopg2.connect(database ="postgres", user='postgres', password='senha', host='localhost', port= '5432')
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute ('CREATE DATABASE mypoke;')
    print('Base de dados mypoke criada com sucesso!')
    # Completa e commita o processo de remoção
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

def deletar_base_de_dados():
    connection = psycopg2.connect(database ="postgres", user='postgres', password='senha', host='localhost', port= '5432')
    connection.autocommit = True
    cursor = connection.cursor()

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
    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    # Executa o comando CREATE do postgresql, caso a tabela pessoas ainda não exista
    #   define os parâmetros de pessoa como 'nome, documento, data_nascimento'
    cursor.execute ("""CREATE TABLE IF NOT EXISTS pessoas (
                        nome VARCHAR,
                        documento BIGINT PRIMARY KEY,
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
    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    # Executa o comando CREATE do postgresql, caso a tabela pokemons ainda não exista
    #   define os parâmetros de pokemon como 'nome, custo_mensal, especie,
    #                                         tipo_primario, tipo_secundario,
    #                                         documento_treinador'
    cursor.execute ("""CREATE TABLE IF NOT EXISTS pokemons (
                        nome VARCHAR PRIMARY KEY,
                        custo_mensal DOUBLE PRECISION,
                        especie VARCHAR,
                        tipo_primario VARCHAR,
                        tipo_secundario VARCHAR,
                        documento_treinador BIGINT REFERENCES pessoas (documento));""")
    # Finaliza e comita a criação de tabela
    connection.commit()

    # Encerra a conexão com o banco de dados
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
    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    # Executa o comando DROP TABLE para ambas as tabelas, caso existam
    cursor.execute ("""DROP TABLE IF EXISTS pessoas CASCADE;""")
    # Finaliza e comita a deleção das tabelas
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
    params = config()
    connection = psycopg2.connect(**params)
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
    
# incluir_pessoa(informacoes)
#   Insere uma pessoa nova no banco de dados
#   Entrada: uma string no formato "nome,documento,data_nascimento"
#   Saída: nenhuma
def incluir_pessoa(entrada):

    # Acessa o banco de dados
    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    # Divide a string de entrada nos parâmetros referentes aos campos da tabela e armazena em 'valores'
    nome, documento, data_nascimento = (entrada.replace(';', '')).split(',')
    valores = "'" + nome + "'" + ", " + "'" + str (documento) + "'" + ", " + "'" + data_nascimento + "'"

    # Executa o comando INSERT em postgresql para inserir a instância na tabela
    cursor.execute ("""INSERT INTO pessoas (nome, documento, data_nascimento)
                     VALUES ("""+ valores + ");")
    # Completa e commita o processo de inserção
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

# incluir_pokemon(informacoes)
#   Insere um pokemon novo no banco de dados
#   Entrada: uma string no formato "nome,custo_mensal,especie,tipo_primario,tipo_secundario,documento_dono"
#   Saída: nenhuma
def incluir_pokemon(entrada):
    
    # Acessa o banco de dados
    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    # Divide a string de entrada nos parâmetros referentes aos campos da tabela e armazena em 'valores'
    nome, custo_mensal, tipo_primario, tipo_secundario, documento_dono, especie = (entrada.replace(';', '')).split(',')
    if tipo_secundario == '':
        tipo_secundario = 'NULL'
    valores = "'" + nome + "'" + ", " + "'" + str (custo_mensal) + "'" + ", " + "'" + tipo_primario + "'" + ", " + "'" + tipo_secundario + "'" + ", " + "'" + str (documento_dono) + "'" + ", " + "'" + especie + "'"

    # Executa o comando INSERT em postgresql para inserir a instância na tabela
    cursor.execute ("""INSERT INTO pokemons (nome, custo_mensal, especie, tipo_primario, tipo_secundario, documento_treinador) 
                    VALUES ("""+ valores + ");")
    # Completa e commita o processo de inserção
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()
    
def atualizar_pessoa(documento, nome, data_nascimento):

    # Acessa o banco de dados
    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    # Determina se o usuário quer fazer a alteração do nome, data de nascimento ou ambos
    #   então, executa o comando UPDATE pessoas SET [] para alterar as colunas em questão
    #   na linha onde 'documento' é igual ao argumento passado
    cursor.execute (""" UPDATE pessoas
                        SET nome = """ + "'" + nome + "'" + ", data_nascimento = " + "'" + data_nascimento + "'" +
                        " WHERE documento = " + "'" + str(documento) + "'" + ";")
    # Completa e commita o processo de alteração da tabela
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()

def selecionar_pessoa(documento):

    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    cursor.execute ("""SELECT * FROM pessoas
                       WHERE documento = """ + str (documento) + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry.pop()

def selecionar_pokemon(nome):

    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    cursor.execute ("""SELECT * FROM pokemons
                       WHERE nome = """ + nome + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry.pop()


def retorna_tabela_pessoas():

    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    cursor.execute ("SELECT * FROM pessoas")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry

def retorna_tabela_pokemons():

    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    cursor.execute ("SELECT * FROM pokemons")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry

def retorna_pokemons_de_pessoa(documento_treinador):

    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    cursor.execute ("""SELECT * FROM pokemons
                       WHERE documento_treinador = """ + str(documento_treinador) + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry

def retorna_pokemons_do_tipo(tipo):

    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    cursor.execute ("""SELECT * FROM pokemons
                       WHERE tipo_primario = """ + "'" + tipo + "'" + " OR tipo_secundario = " + "'" + tipo + "'" + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry

def retorna_pokemons_da_especie(especie):

    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    cursor.execute ("""SELECT * FROM pokemons
                       WHERE especie = """ + "'" + especie + "'" + ";")
    resultado_querry = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return resultado_querry

# excluir_pessoa(documento)
#   Exclui a pessoa com a chave primaria 'documento'
#   Entrada: uma string que contém o número de documento da pessoa a ser excluida
#   Saída: nenhuma
def excluir_pessoa(documento):
    
    # Acessa o banco de dados
    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    # Executa o comando DELETE em postgresql para remover a instância na tabela com a chave primária 'documento' igual ao argumento
    cursor.execute ("DELETE FROM pokemons WHERE documento_treinador = " + "'" + str (documento) + "'" + ";")
    cursor.execute ("DELETE FROM pessoas WHERE documento = " + "'" + str (documento) + "'" + ";")
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
    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    # Executa o comando DELETE em postgresql para remover a instância na tabela com a chave primária 'nome_pokemon' igual ao argumento
    cursor.execute ("DELETE FROM pokemons WHERE nome = " + "'" + nome_pokemon + "'" + ";")
    # Completa e commita o processo de remoção
    connection.commit()

    # Encerra a conexão com o banco de dados
    cursor.close()
    connection.close()





#################################################################################
# COMANDOS DE TESTE
# TODO: REMOVER

def main():
    #deletar_base_de_dados()
    criar_base_de_dados()
    criar_tabela_pessoas()
    criar_tabela_pokemons()
    incluir_pessoa ('Rafa,555551278,21/03/1999;')
    incluir_pessoa ('Lucas,665551278,16/06/1998;')
    incluir_pokemon('Mayu,150.00,Charizard,Fogo,Voador,665551278;')
    incluir_pokemon('Charla,150.00,Charizard,Fogo,Voador,555551278;')
    incluir_pokemon('Aurora,65.50,Butterfree,Inseto,Voador,555551278;')
    incluir_pokemon('Ghastly,100.50,Ghastly,Fantasma,,555551278;')
    incluir_pokemon('Rafa Zapdos,600,Zapdos,Voador,Elétrico,555551278;')
    #excluir_pokemon ("Charla")
    #excluir_pessoa (555551278)
    atualizar_pessoa(555551278,'Rafa','24/03/1999')
    #reiniciar_tabela('pessoas')
    #print (retorna_tabela_pokemons())
    #print (selecionar_pessoa(555551278))
    #print (retorna_pokemons_de_pessoa(555551278))
    pokemons_voadores = retorna_pokemons_do_tipo('Voador')
    pokemons_voadores.sort(key=lambda x:x[1])
    print (pokemons_voadores)
    excluir_pessoa (555551278)
    print (retorna_tabela_pokemons())
    print (retorna_tabela_pessoas())
    deletar_base_de_dados()
    return

if __name__ == "__main__":
    main()
