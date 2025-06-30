import os
from sqlite3 import Connection, Cursor
from typing import Optional
from util.database import obter_conexao
from models.categoria import Categoria
from sql.produto_sql import *
from models.produto import Produto

def criar_tabela_produtos() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de produtos
            cursor.execute(CREATE_TABLE_PRODUTO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de produtos: {e}")
        # Retorna False indicando falha
        return False
    
def inserir_produto(produto: Produto) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir produto com todos os campos
        cursor.execute(INSERT_PRODUTO, 
            (produto.nome, produto.descricao, produto.preco, produto.estoque, produto.imagem, produto.id_categoria))
        # Retorna o ID do produto inserido
        return cursor.lastrowid

def atualizar_produto(produto: Produto) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar todos os campos do produto pelo ID
        cursor.execute(UPDATE_PRODUTO, 
            (produto.nome, produto.descricao, produto.preco, produto.estoque, produto.imagem, produto.id_categoria, produto.id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_produto(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar produto pelo ID
        cursor.execute(DELETE_PRODUTO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def obter_produto_por_id(id: int) -> Optional[Produto]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar produto pelo ID com join na categoria
        cursor.execute(GET_PRODUTO_BY_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Produto com dados do banco
            return Produto(
                id=resultado["id"],
                nome=resultado["nome"],
                descricao=resultado["descricao"],
                preco=resultado["preco"],
                estoque=resultado["estoque"],
                imagem=resultado["imagem"],
                id_categoria=resultado["id_categoria"],
                # Cria objeto Categoria associado ao produto
                categoria=Categoria(
                    id=resultado["id_categoria"],
                    nome=resultado["nome_categoria"]
                )
            )
    # Retorna None se não encontrou produto
    return None

def obter_produtos_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Produto]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar produtos com paginação e join na categoria
        cursor.execute(GET_PRODUTOS_BY_PAGE, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Produto a partir dos resultados
        return [Produto(
            id=resultado["id"],
            nome=resultado["nome"],
            descricao=resultado["descricao"],
            preco=resultado["preco"],
            estoque=resultado["estoque"],
            imagem=resultado["imagem"],
            id_categoria=resultado["id_categoria"],
            # Cria objeto Categoria associado a cada produto
            categoria=Categoria(
                id=resultado["id_categoria"],
                nome=resultado["nome_categoria"]
            )
        ) for resultado in resultados]
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    # Verifica se já existem produtos na tabela
    lista = obter_produtos_por_pagina(1, 5)
    # Se já houver produtos, não faz nada
    if lista: 
        return
    # Constrói caminho para arquivo SQL com dados iniciais
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_produtos.sql')
    # Abre arquivo SQL para leitura
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        # Lê conteúdo do arquivo SQL
        sql_inserts = arquivo.read()
        # Executa comandos SQL de inserção
        conexao.execute(sql_inserts)
