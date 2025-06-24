from fastapi.responses import RedirectResponse
import uvicorn
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from babel.numbers import format_currency
from starlette.middleware.sessions import SessionMiddleware

from models.usuario import Usuario
from repo import usuario_repo
from repo.categoria_repo import criar_tabela_categorias, obter_categorias_por_pagina
from repo.usuario_repo import criar_tabela_usuarios, obter_usuarios_por_pagina
from repo.endereco_repo import criar_tabela_enderecos, obter_enderecos_por_pagina
from repo.produto_repo import criar_tabela_produtos, obter_produto_por_id, obter_produtos_por_pagina
from util.auth import SECRET_KEY, autenticar_usuario, hash_senha

criar_tabela_produtos()
criar_tabela_usuarios()
criar_tabela_categorias()
criar_tabela_enderecos()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

def format_currency_br(value, currency='BRL', locale='pt_BR'):
    return format_currency(value, currency, locale=locale)

templates.env.filters['format_currency_br'] = format_currency_br

@app.get("/")
def read_root(request: Request):
    produtos = obter_produtos_por_pagina(1, 12)
    response = templates.TemplateResponse("index.html", {"request": request, "produtos": produtos })
    return response

@app.get("/produtos/{id}")
def read_produto(request: Request, id: int):
    produto = obter_produto_por_id(id)
    response = templates.TemplateResponse("produto.html", {"request": request, "produto": produto})
    return response

@app.get("/usuarios")
def read_usuarios(request: Request):
    usuarios = obter_usuarios_por_pagina(1, 12)
    response = templates.TemplateResponse("usuarios.html", {"request": request, "usuarios": usuarios})
    return response

@app.get("/produtos")
def read_produtos(request: Request):
    produtos = obter_produtos_por_pagina(1, 12)
    response = templates.TemplateResponse("produtos.html", {"request": request, "produtos": produtos})
    return response

@app.get("/categorias")
def read_categorias(request: Request):
    categorias = obter_categorias_por_pagina(1, 12)
    response = templates.TemplateResponse("categorias.html", {"request": request, "categorias": categorias})
    return response

@app.get("/enderecos")
def read_enderecos(request: Request):
    enderecos = obter_enderecos_por_pagina(1, 12)
    response = templates.TemplateResponse("enderecos.html", {"request": request, "enderecos": enderecos})
    return response

@app.get("/cadastrar")
def read_cadastrar(request: Request):
    return templates.TemplateResponse("cadastrar.html", {"request": request})

@app.post("/cadastrar")
async def cadastrar_usuario(
    request: Request,
    nome: str = Form(),
    cpf: str = Form(),
    email: str = Form(),
    telefone: str = Form(),
    data_nascimento: str = Form(),
    senha: str = Form(),
    conf_senha: str = Form()
):
    if senha != conf_senha:
        raise HTTPException(status_code=400, detail="As senhas não conferem")
    usuario = Usuario(
        id=0,
        nome=nome,
        cpf=cpf,
        telefone=telefone,
        email=email,
        data_nascimento=data_nascimento,
        senha_hash=hash_senha(senha),
        tipo=0
    )
    usuario = usuario_repo.inserir_usuario(usuario)
    if not usuario:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar usuário")
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login")
def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request, 
    email: str = Form(), 
    senha: str = Form()):
    usuario = autenticar_usuario(email, senha)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    usuario_json = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": "admin" if usuario.tipo==1 else "user"
    }
    request.session["usuario"] = usuario_json
    return RedirectResponse(url="/", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@app.get("/usuarios/promover/{id}")
async def promover_usuario(request: Request, id: int):
    usuario = usuario_repo.obter_usuario_por_id(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario_repo.atualizar_tipo_usuario(id, 1)
    return RedirectResponse(url="/usuarios", status_code=303)

@app.get("/usuarios/rebaixar/{id}")
async def promover_usuario(request: Request, id: int):
    usuario = usuario_repo.obter_usuario_por_id(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario_repo.atualizar_tipo_usuario(id, 0)
    return RedirectResponse(url="/usuarios", status_code=303)

@app.get("/perfil")
async def perfil_usuario(request: Request):
    # Captura os dados do usuário da sessão (logado)
    usuario_json = request.session.get("usuario")
    # Se não encontrou um usuário, retorna erro 401
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    # Busca os dados do usuário no repositório
    usuario = usuario_repo.obter_usuario_por_id(usuario_json["id"])
    # Se não encontrou o usuário, retorna erro 404
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # Retorna a página de perfil com os dados do usuário
    return templates.TemplateResponse("perfil.html", {"request": request, "perfil": usuario})

@app.post("/perfil")
async def atualizar_perfil(
    request: Request,
    nome: str = Form(),
    telefone: str = Form(),
    email: str = Form(),
    data_nascimento: str = Form()
):
    # Captura os dados do usuário da sessão (logado)
    usuario_json = request.session.get("usuario")
    # Se não encontrou um usuário, retorna erro 401
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    # Busca os dados do usuário no repositório
    usuario = usuario_repo.obter_usuario_por_id(usuario_json["id"])
    # Se não encontrou o usuário, retorna erro 404
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # Atualiza os dados do usuário
    usuario.nome = nome
    usuario.telefone = telefone
    usuario.email = email
    usuario.data_nascimento = data_nascimento
    # Atualiza o usuário no repositório
    if not usuario_repo.atualizar_usuario(usuario):
        raise HTTPException(status_code=400, detail="Erro ao atualizar perfil")
    # Atualiza os dados do usuário na sessão
    usuario_json = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": "admin" if usuario.tipo==1 else "user"
    }
    request.session["usuario"] = usuario_json
    # Redireciona para a página de perfil
    return RedirectResponse(url="/perfil", status_code=303)

@app.get("/senha")
async def senha_usuario(request: Request):
    # Captura os dados do usuário da sessão (logado)
    usuario_json = request.session.get("usuario")
    # Se não encontrou um usuário, retorna erro 401
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    # Busca os dados do usuário no repositório
    usuario = usuario_repo.obter_usuario_por_id(usuario_json["id"])
    # Se não encontrou o usuário, retorna erro 404
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # Retorna a página de senha com os dados do usuário
    return templates.TemplateResponse("senha.html", {"request": request})

@app.post("/senha")
async def atualizar_senha(
    request: Request,    
    nova_senha: str = Form(),
    conf_nova_senha: str = Form()
):
    # Captura os dados do usuário da sessão (logado)
    usuario_json = request.session.get("usuario")
    # Se não encontrou um usuário, retorna erro 401
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    # Busca os dados do usuário no repositório
    usuario = usuario_repo.obter_usuario_por_id(usuario_json["id"])
    # Se não encontrou o usuário, retorna erro 404
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # Verifica se as senhas conferem
    if nova_senha != conf_nova_senha:
        raise HTTPException(status_code=400, detail="As senhas não conferem")
    # Atualiza a senha do usuário
    if not usuario_repo.atualizar_senha_usuario(usuario.id, hash_senha(nova_senha)):
        raise HTTPException(status_code=400, detail="Erro ao atualizar senha")
    # Redireciona para a página de perfil
    return RedirectResponse(url="/perfil", status_code=303)

if __name__ == "__main__":
    uvicorn.run(app=app, port=8000, reload=True)