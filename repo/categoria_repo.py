import os
from sqlite3 import Connection
from typing import Optional
from util.database import obter_conexao
from sql.categoria_sql import *
from models.categoria import Categoria

def criar_tabela_categorias() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CREATE_TABLE_CATEGORIA)
            inserir_dados_iniciais(conexao)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False

def inserir_categoria(categoria: Categoria) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERT_CATEGORIA, 
            (categoria.nome,))
        return cursor.lastrowid

def atualizar_categoria(categoria: Categoria) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(UPDATE_CATEGORIA, 
            (categoria.nome, categoria.id))
        return (cursor.rowcount > 0)

def excluir_categoria(id: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(DELETE_CATEGORIA, (id,))
        return (cursor.rowcount > 0)

def obter_categoria_por_id(id: int) -> Optional[Categoria]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(GET_CATEGORIA_BY_ID, (id,))
        resultado = cursor.fetchone()
        if resultado:
            return Categoria(
                id=resultado["id"],
                nome=resultado["nome"])
    return None

def obter_categorias_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Categoria]:
    with obter_conexao() as conexao:
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor = conexao.cursor()
        cursor.execute(GET_CATEGORIAS_BY_PAGE, (limite, offset))
        resultados = cursor.fetchall()
        return [Categoria(
            id=resultado["id"],
            nome=resultado["nome"])
            for resultado in resultados]
    
def inserir_dados_iniciais(conexao: Connection):
    # Verifica se já existem categorias na tabela
    lista = obter_categorias_por_pagina(1, 5)
    if lista: 
        return
    # Se não houver categorias, insere os dados iniciais    
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)    
        conexao.commit()
        conexao.close()