from datetime import datetime
import os
from sqlite3 import Connection, Cursor
from typing import Optional
from util.database import obter_conexao
from sql.usuario_sql import *
from models.usuario import Usuario

def criar_tabela_usuarios() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de usuários
            cursor.execute(CREATE_TABLE_USUARIO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de usuários: {e}")
        # Retorna False indicando falha
        return False

def inserir_usuario(usuario: Usuario) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir usuário com todos os campos
        cursor.execute(INSERT_USUARIO, 
            (usuario.nome, usuario.cpf, usuario.telefone, usuario.email, usuario.data_nascimento, usuario.senha_hash))
        # Retorna o ID do usuário inserido
        return cursor.lastrowid        

def atualizar_usuario(usuario: Usuario) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do usuário pelo ID
        cursor.execute(UPDATE_USUARIO, 
            (usuario.nome, usuario.cpf, usuario.telefone, usuario.email, usuario.data_nascimento, usuario.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)
    
def atualizar_tipo_usuario(id: int, tipo: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar tipo do usuário (0=comum, 1=admin)
        cursor.execute(UPDATE_TIPO_USUARIO, (tipo, id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)
    
def atualizar_senha_usuario(id: int, senha_hash: str) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar senha hash do usuário
        cursor.execute(UPDATE_SENHA_USUARIO, (senha_hash, id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_usuario(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar usuário pelo ID
        cursor.execute(DELETE_USUARIO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)    

def obter_usuario_por_id(id: int) -> Optional[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuário pelo ID
        cursor.execute(GET_USUARIO_BY_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Usuario com dados do banco
            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                email=resultado["email"],
                # Converte string de data para objeto date
                data_nascimento=datetime.strptime(resultado["data_nascimento"], "%Y-%m-%d").date(),
                senha_hash=resultado["senha_hash"],
                tipo=resultado["tipo"])
    # Retorna None se não encontrou usuário
    return None

def obter_usuario_por_email(email: str) -> Optional[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuário pelo email
        cursor.execute(GET_USUARIO_BY_EMAIL, (email,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Usuario com dados do banco
            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                email=resultado["email"],
                # Converte string de data para objeto date
                data_nascimento=datetime.strptime(resultado["data_nascimento"], "%Y-%m-%d").date(),
                senha_hash=resultado["senha_hash"],
                tipo=resultado["tipo"])
    # Retorna None se não encontrou usuário
    return None

def obter_usuarios_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuários com paginação
        cursor.execute(GET_USUARIOS_BY_PAGE, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Usuario a partir dos resultados
        return [Usuario(
            id=resultado["id"],
            nome=resultado["nome"],
            cpf=resultado["cpf"],
            telefone=resultado["telefone"],
            email=resultado["email"],
            # Converte string de data para objeto date
            data_nascimento=datetime.strptime(resultado["data_nascimento"], "%Y-%m-%d").date(),
            tipo=resultado["tipo"]
        ) for resultado in resultados]
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    # Verifica se já existem usuários na tabela
    lista = obter_usuarios_por_pagina(1, 5)
    # Se já houver usuários, não faz nada
    if lista: 
        return
    # Constrói caminho para arquivo SQL com dados iniciais
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_usuarios.sql')
    # Abre arquivo SQL para leitura
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        # Lê conteúdo do arquivo SQL
        sql_inserts = arquivo.read()
        # Executa comandos SQL de inserção
        conexao.execute(sql_inserts)