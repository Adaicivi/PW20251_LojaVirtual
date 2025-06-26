from datetime import datetime
import os
from typing import Optional
from util.database import obter_conexao
from sql.usuario_sql import *
from models.usuario import Usuario

def criar_tabela_usuarios() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CREATE_TABLE_USUARIO)
            inserir_dados_iniciais(conexao)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de usuários: {e}")
        return False

def inserir_usuario(usuario: Usuario) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERT_USUARIO, 
            (usuario.nome, usuario.cpf, usuario.telefone, usuario.email, usuario.data_nascimento, usuario.senha_hash))
        return cursor.lastrowid        

def atualizar_usuario(usuario: Usuario) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(UPDATE_USUARIO, 
            (usuario.nome, usuario.cpf, usuario.telefone, usuario.email, usuario.data_nascimento, usuario.id))    
        return (cursor.rowcount > 0)
    
def atualizar_tipo_usuario(id: int, tipo: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(UPDATE_TIPO_USUARIO, (tipo, id))
        return (cursor.rowcount > 0)
    
def atualizar_senha_usuario(id: int, senha_hash: str) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(UPDATE_SENHA_USUARIO, (senha_hash, id))
        return (cursor.rowcount > 0)

def excluir_usuario(id: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(DELETE_USUARIO, (id,))
        return (cursor.rowcount > 0)    

def obter_usuario_por_id(id: int) -> Optional[Usuario]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(GET_USUARIO_BY_ID, (id,))
        resultado = cursor.fetchone()
        if resultado:
            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                email=resultado["email"],
                data_nascimento=datetime.strptime(resultado["data_nascimento"], "%Y-%m-%d").date(),
                senha_hash=resultado["senha_hash"],
                tipo=resultado["tipo"])
    return None

def obter_usuario_por_email(email: str) -> Optional[Usuario]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(GET_USUARIO_BY_EMAIL, (email,))
        resultado = cursor.fetchone()
        if resultado:
            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                email=resultado["email"],
                data_nascimento=datetime.strptime(resultado["data_nascimento"], "%Y-%m-%d").date(),
                senha_hash=resultado["senha_hash"],
                tipo=resultado["tipo"])
    return None

def obter_usuarios_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Usuario]:
    with obter_conexao() as conexao:
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor = conexao.cursor()
        cursor.execute(GET_USUARIOS_BY_PAGE, (limite, offset))
        resultados = cursor.fetchall()
        return [Usuario(
            id=resultado["id"],
            nome=resultado["nome"],
            cpf=resultado["cpf"],
            telefone=resultado["telefone"],
            email=resultado["email"],
            data_nascimento=datetime.strptime(resultado["data_nascimento"], "%Y-%m-%d").date(),
            tipo=resultado["tipo"]
        ) for resultado in resultados]
    
def inserir_dados_iniciais(conexao):
    # Verifica se já existem usuários na tabela
    lista = obter_usuarios_por_pagina(1, 5)
    if lista: 
        return
    # Se não houver usuários, insere os dados iniciais    
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_usuarios.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)