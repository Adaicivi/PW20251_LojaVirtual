from datetime import datetime
from typing import Optional
from data.database import obter_conexao
from sql.usuario_sql import *
from models.usuario import Usuario

def criar_tabela_usuarios() -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(CREATE_TABLE_USUARIO)        
        return (cursor.rowcount > 0)

def inserir_usuario(usuario: Usuario) -> Usuario:    
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERT_USUARIO, 
            (usuario.nome, usuario.cpf, usuario.telefone, usuario.email, usuario.data_nascimento, usuario.senha_hash))
        usuario.id = cursor.lastrowid
        return usuario

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