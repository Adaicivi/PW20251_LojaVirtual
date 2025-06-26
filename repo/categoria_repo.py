import os
from sqlite3 import Connection, Cursor
from typing import Optional
from util.database import obter_conexao
from sql.categoria_sql import *
from models.categoria import Categoria

def criar_tabela_categorias() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de categorias
            cursor.execute(CREATE_TABLE_CATEGORIA)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de categorias: {e}")
        # Retorna False indicando falha
        return False

def inserir_categoria(categoria: Categoria) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir categoria com o nome fornecido
        cursor.execute(INSERT_CATEGORIA, 
            (categoria.nome,))
        # Retorna o ID da categoria inserida
        return cursor.lastrowid

def atualizar_categoria(categoria: Categoria) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar nome da categoria pelo ID
        cursor.execute(UPDATE_CATEGORIA, 
            (categoria.nome, categoria.id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_categoria(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar categoria pelo ID
        cursor.execute(DELETE_CATEGORIA, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def obter_categoria_por_id(id: int) -> Optional[Categoria]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar categoria pelo ID
        cursor.execute(GET_CATEGORIA_BY_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Categoria com dados do banco
            return Categoria(
                id=resultado["id"],
                nome=resultado["nome"])
    # Retorna None se não encontrou categoria
    return None

def obter_categorias_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Categoria]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar categorias com paginação
        cursor.execute(GET_CATEGORIAS_BY_PAGE, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Categoria a partir dos resultados
        return [Categoria(
            id=resultado["id"],
            nome=resultado["nome"])
            for resultado in resultados]
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    # Verifica se já existem categorias na tabela
    lista = obter_categorias_por_pagina(1, 5)
    # Se já houver categorias, não faz nada
    if lista: 
        return
    # Constrói caminho para arquivo SQL com dados iniciais
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    # Abre arquivo SQL para leitura
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        # Lê conteúdo do arquivo SQL
        sql_inserts = arquivo.read()
        # Executa comandos SQL de inserção
        conexao.execute(sql_inserts)
