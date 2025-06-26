import os
from sqlite3 import Connection, Cursor
from typing import Optional
from util.database import obter_conexao
from sql.endereco_sql import *
from models.endereco import Endereco

def criar_tabela_enderecos() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de endereços
            cursor.execute(CREATE_TABLE_ENDERECO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de endereços: {e}")
        # Retorna False indicando falha
        return False

def inserir_endereco(endereco: Endereco) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir endereço com todos os campos
        cursor.execute(INSERT_ENDERECO, (
            endereco.logradouro, 
            endereco.numero,
            endereco.complemento,
            endereco.bairro,
            endereco.cidade,
            endereco.estado,
            endereco.cep,
            endereco.id_usuario))
        # Retorna o ID do endereço inserido
        return cursor.lastrowid

def atualizar_endereco(endereco: Endereco) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar todos os campos do endereço pelo ID
        cursor.execute(UPDATE_ENDERECO, (
            endereco.logradouro,
            endereco.numero,
            endereco.complemento,
            endereco.bairro,
            endereco.cidade,
            endereco.estado,
            endereco.cep,
            endereco.id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_endereco(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar endereço pelo ID
        cursor.execute(DELETE_ENDERECO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def obter_endereco_por_id(id: int) -> Optional[Endereco]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar endereço pelo ID
        cursor.execute(GET_ENDERECO_BY_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Endereco com dados do banco
            return Endereco(
                id=resultado["id"],
                logradouro=resultado["logradouro"],
                numero=resultado["numero"],
                complemento=resultado["complemento"],
                bairro=resultado["bairro"],
                cidade=resultado["cidade"],
                estado=resultado["estado"],
                cep=resultado["cep"],
                id_usuario=resultado["id_usuario"])
    # Retorna None se não encontrou endereço
    return None

def obter_enderecos_por_usuario(id_usuario: int) -> list[Endereco]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar todos endereços de um usuário
        cursor.execute(GET_ENDERECOS_BY_ID_USUARIO, (id_usuario,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Endereco a partir dos resultados
        return [Endereco(
            id=resultado["id"],
            logradouro=resultado["logradouro"],
            numero=resultado["numero"],
            complemento=resultado["complemento"],
            bairro=resultado["bairro"],
            cidade=resultado["cidade"],
            estado=resultado["estado"],
            cep=resultado["cep"],
            id_usuario=resultado["id_usuario"]
        ) for resultado in resultados]
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    # Verifica se já existem endereços na tabela
    lista = obter_enderecos_por_usuario(1)
    # Se já houver endereços, não faz nada
    if lista: 
        return
    # Constrói caminho para arquivo SQL com dados iniciais
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_enderecos.sql')
    # Abre arquivo SQL para leitura
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        # Lê conteúdo do arquivo SQL
        sql_inserts = arquivo.read()
        # Executa comandos SQL de inserção
        conexao.execute(sql_inserts)
        