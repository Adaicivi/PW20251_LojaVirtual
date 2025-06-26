from typing import Optional
from data.database import obter_conexao
from sql.endereco_sql import *
from models.endereco import Endereco

def criar_tabela_enderecos() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CREATE_TABLE_ENDERECO)
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