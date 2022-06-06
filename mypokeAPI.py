#####################################################################
# myPokeAPI.py - API de manutenção do banco de dados myPoké
#
# Contribuidores: Lucas Emery
#                 Thiago Damasceno
#
# Funcionalidade:
#    Esse arquivo contém as funções do CRUD do banco de dados myPoké
#    a partir dele, consegue-se criar, remover, editar e deletar entidades
#    das classes Pessoa e Pokémon.
#####################################################################

# psycopg2: ferramenta utilizada para fazer a ponte entre posgresql e python
import psycopg2
from databaseconfig import config

# inserir_pessoa(informacoes)
#   Insere uma pessoa nova no banco de dados
#   Entrada: uma string no formato "nome,documento,data_nascimento"
#   Saída: nenhuma
def inserir_pessoa(nome, documento, data_nascimento):

    # Acessa o banco de dados
    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    # Divide a string de entrada nos parâmetros referentes aos campos da tabela e armazena em 'valores'
    valores = "'" + nome + "'" + ", " + "'" + str (documento) + "'" + ", " + "'" + data_nascimento + "'"

    # Executa o comando INSERT em postgresql para inserir a instância na tabela
    cursor.execute ("""INSERT INTO pessoas (nome, documento, data_nascimento)
                     VALUES ("""+ valores + ");")
    # Completa e commita o processo de inserção
    connection.commit()

    # Fecha a conexão com o banco de dados
    cursor.close()
    connection.close()

# inserir_pokemon(informacoes)
#   Insere um pokemon novo no banco de dados
#   Entrada: uma string no formato "nome,custo_mensal,especie,tipo_primario,tipo_secundario,documento_dono"
#   Saída: nenhuma
def inserir_pokemon(nome, custo_mensal, tipo_primario, tipo_secundario, documento_dono, especie):
    
    # Acessa o banco de dados
    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    # Divide a string de entrada nos parâmetros referentes aos campos da tabela e armazena em 'valores'
    valores = "'" + nome + "'" + ", " + "'" + str (custo_mensal) + "'" + ", " + "'" + tipo_primario + "'" + ", " + "'" + tipo_secundario + "'" + ", " + "'" + str (documento_dono) + "'" + ", " + "'" + especie + "'"

    # Executa o comando INSERT em postgresql para inserir a instância na tabela
    cursor.execute ("""INSERT INTO pokemons (nome, custo_mensal, tipo_primario, tipo_secundario, documento_dono, especie) 
                    VALUES ("""+ valores + ");")
    # Completa e commita o processo de inserção
    connection.commit()

    # Fecha a conexão com o banco de dados
    cursor.close()
    connection.close()

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
    cursor.execute ("DELETE FROM pessoas WHERE documento = " + "'" + str (documento) + "'" + ";")
    # Completa e commita o processo de remoção
    connection.commit()

    # Fecha a conexão com o banco de dados
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

    # Fecha a conexão com o banco de dados
    cursor.close()
    connection.close()





#################################################################################
# COMANDOS DE TESTE
# TODO: REMOVER

def main():
    #inserir_pokemon("Charla", 150.00, 'Fogo', 'Voador', 555551234, 'Charizard')
    #inserir_pessoa ("Rafa", 555551278, '21/03/1999')
    #excluir_pokemon ("Charla")
    #excluir_pessoa (555551278)

if __name__ == "__main__":
    main()
