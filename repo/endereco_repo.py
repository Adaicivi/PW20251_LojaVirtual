import os
from typing import Optional
from util.database import obter_conexao
from sql.endereco_sql import *
from models.endereco import Endereco

def criar_tabela_enderecos() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CREATE_TABLE_ENDERECO)
            inserir_dados_iniciais(conexao)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de endereços: {e}")
        return False

def inserir_endereco(endereco: Endereco) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERT_ENDERECO, (
            endereco.logradouro, 
            endereco.numero,
            endereco.complemento,
            endereco.bairro,
            endereco.cidade,
            endereco.estado,
            endereco.cep,
            endereco.id_usuario))
        return cursor.lastrowid

def atualizar_endereco(endereco: Endereco) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(UPDATE_ENDERECO, (
            endereco.logradouro,
            endereco.numero,
            endereco.complemento,
            endereco.bairro,
            endereco.cidade,
            endereco.estado,
            endereco.cep,
            endereco.id))
        return (cursor.rowcount > 0)

def excluir_endereco(id: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(DELETE_ENDERECO, (id,))
        return (cursor.rowcount > 0)

def obter_endereco_por_id(id: int) -> Optional[Endereco]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(GET_ENDERECO_BY_ID, (id,))
        resultado = cursor.fetchone()
        if resultado:
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
    return None

def obter_enderecos_por_usuario(id_usuario: int) -> list[Endereco]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(GET_ENDERECOS_BY_ID_USUARIO, (id_usuario,))
        resultados = cursor.fetchall()
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
    
def inserir_dados_iniciais(conexao):
    # Verifica se já existem endereços na tabela
    lista = obter_enderecos_por_usuario(1)
    if lista: 
        return
    # Se não houver endereços, insere os dados iniciais    
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_enderecos.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)