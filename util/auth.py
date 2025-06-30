from typing import Optional
from fastapi import HTTPException, Request
import hashlib

from models.usuario import Usuario
from repo import usuario_repo

# Chave secreta utilizada para criptografia de sessões
SECRET_KEY="cae3def7c5c8f5c07613a742c1c5435076ccf0777c259796ad1653c0fd5dfdd7"

def hash_senha(senha: str) -> str:
    # Converte a senha para bytes e aplica hash SHA256
    # Retorna o hash como string hexadecimal
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha_normal: str, senha_hashed: str) -> bool:
    # Gera hash da senha fornecida e compara com o hash armazenado
    # Retorna True se as senhas coincidem, False caso contrário
    return hash_senha(senha_normal) == senha_hashed

def autenticar_usuario(email: str, senha: str):
    # Busca usuário no banco de dados pelo email
    usuario = usuario_repo.obter_usuario_por_email(email)
    # Verifica se usuário existe e se a senha está correta
    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        # Retorna None se autenticação falhar
        return None
    # Retorna o objeto usuário se autenticação for bem-sucedida
    return usuario

def obter_usuario_logado(request: Request) -> Optional[Usuario]:
    # Obtém dados do usuário da sessão HTTP
    usuario = request.session.get("usuario")
    # Verifica se existe usuário na sessão
    if not usuario:
        # Lança exceção HTTP 401 se não houver usuário autenticado
        raise HTTPException(status_code=401, detail="Não autenticado")
    # Retorna os dados do usuário logado
    return usuario
