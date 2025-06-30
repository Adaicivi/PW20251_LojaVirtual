from fastapi.responses import RedirectResponse
import uvicorn
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from babel.numbers import format_currency
from starlette.middleware.sessions import SessionMiddleware

from models.categoria import Categoria
from models.usuario import Usuario
from repo import usuario_repo, endereco_repo, categoria_repo, produto_repo
from util import initializer
from util.auth import SECRET_KEY, autenticar_usuario, hash_senha

# Cria as tabelas no banco de dados se não existirem
initializer.criar_tabelas()
# Insere dados iniciais no banco de dados
initializer.inserir_dados_iniciais()

# Cria a instância do FastAPI para a aplicacão web
app = FastAPI()
# Configura o Jinja2 para renderizar templates HTML
templates = Jinja2Templates(directory="templates")
# Adiciona o middleware de sessão para gerenciar sessões de usuário
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Filtro para formatar valores monetários em reais (BRL) usando Babel
def format_currency_br(value, currency='BRL', locale='pt_BR'):
    return format_currency(value, currency, locale=locale)

# Registra o filtro de formatação de moeda brasileira no Jinja2
templates.env.filters['format_currency_br'] = format_currency_br

@app.get("/")
def read_root(request: Request):
    # Obtém os primeiros 12 produtos do banco de dados
    produtos = produto_repo.obter_produtos_por_pagina(1, 12)
    # Cria uma página inicial com os produtos capturados
    response = templates.TemplateResponse("index.html", {"request": request, "produtos": produtos })
    # Retorna a página inicial com os produtos
    return response

@app.get("/produtos/{id}")
def read_produto(request: Request, id: int):
    # Obtém um produto específico do banco de dados pelo ID
    produto = produto_repo.obter_produto_por_id(id)
    # Cria uma página com o produto capturado
    response = templates.TemplateResponse("produto.html", {"request": request, "produto": produto})
    # Retorna a página com o produto
    return response

@app.get("/usuarios")
def read_usuarios(request: Request):
    # Obtém os primeiros 12 usuários do banco de dados
    usuarios = usuario_repo.obter_usuarios_por_pagina(1, 12)
    # Cria uma página com os usuários capturados
    response = templates.TemplateResponse("usuarios.html", {"request": request, "usuarios": usuarios})
    # Retorna a página com os usuários
    return response

@app.get("/produtos")
def read_produtos(request: Request):
    # Obtém os primeiros 12 produtos do banco de dados
    produtos = produto_repo.obter_produtos_por_pagina(1, 12)
    # Cria uma página com os produtos capturados
    response = templates.TemplateResponse("produtos.html", {"request": request, "produtos": produtos})
    # Retorna a página com os produtos
    return response

@app.get("/categorias")
def read_categorias(request: Request):
    # Obtém as primeiras 12 categorias do banco de dados
    categorias = categoria_repo.obter_categorias_por_pagina(1, 12)
    # Cria uma página com as categorias capturadas
    response = templates.TemplateResponse("categorias.html", {"request": request, "categorias": categorias})
    # Retorna a página com as categorias
    return response

@app.get("/enderecos/{id_usuario}")
def read_enderecos(request: Request, id_usuario: int):
    # Obtém os endereços de um usuário específico do banco de dados
    enderecos = endereco_repo.obter_enderecos_por_usuario(id_usuario)
    # Cria uma página com os endereços do usuário
    response = templates.TemplateResponse("enderecos.html", {"request": request, "enderecos": enderecos})
    # Retorna a página com os endereços
    return response

@app.get("/cadastrar")
def read_cadastrar(request: Request):
    # Retorna a página de cadastro de usuário
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
    # Se a senha e a confirmação de senha são diferentes, retorna erro 400
    if senha != conf_senha:
        raise HTTPException(status_code=400, detail="As senhas não conferem")
    # Cria um objeto Usuario com os dados informados
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
    # Tenta inserir o usuário no repositório
    usuario = usuario_repo.inserir_usuario(usuario)
    # Se não conseguiu inserir o usuário, retorna erro 400
    if not usuario:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar usuário")
    # Se conseguiu inserir o usuário, redireciona para a página de login
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login")
def read_login(request: Request):
    # Retorna a página de login
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request, 
    email: str = Form(), 
    senha: str = Form()):
    # Verifica se o email e senha informados estão corretos
    usuario = autenticar_usuario(email, senha)
    # Se não encontrou o usuário com as credenciais, retorna erro 401
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    # Se encontrou o usuário, cria um objeto JSON com os dados do usuário
    usuario_json = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": "admin" if usuario.tipo==1 else "user"
    }
    # Armazena os dados do usuário na sessão
    request.session["usuario"] = usuario_json
    # Redireciona para a página inicial
    return RedirectResponse(url="/", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    # Limpa a sessão do usuário
    request.session.clear()
    # Redireciona para a página inicial
    return RedirectResponse(url="/", status_code=303)

@app.get("/usuarios/promover/{id}")
async def promover_usuario(request: Request, id: int):
    # Busca o usuário pelo ID
    usuario = usuario_repo.obter_usuario_por_id(id)
    # Se não encontrou o usuário, retorna erro 404
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # Promove o usuário para tipo 1 (administrador)
    usuario_repo.atualizar_tipo_usuario(id, 1)
    # Redireciona para a lista de usuários
    return RedirectResponse(url="/usuarios", status_code=303)

@app.get("/usuarios/rebaixar/{id}")
async def promover_usuario(request: Request, id: int):
    # Busca o usuário pelo ID
    usuario = usuario_repo.obter_usuario_por_id(id)
    # Se não encontrou o usuário, retorna erro 404
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # Rebaixa o usuário para tipo 0 (usuário comum)
    usuario_repo.atualizar_tipo_usuario(id, 0)
    # Redireciona para a lista de usuários
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

@app.get("/categorias/inserir")
async def inserir_categoria(request: Request):
    # Retorna a página de inserção de categoria
    return templates.TemplateResponse("inserir_categoria.html", {"request": request})

@app.post("/categorias/inserir")
async def inserir_categoria_post(
    request: Request,
    nome: str = Form()
):
    # Se nome não for informado, retorna erro 400
    if not nome:
        raise HTTPException(status_code=400, detail="Nome é obrigatório")
    # Cria um objeto Categoria com os dados informados
    categoria = Categoria(0, nome)
    # Tenta inserir a categoria no repositório
    if not categoria_repo.inserir_categoria(categoria):
        raise HTTPException(status_code=400, detail="Erro ao inserir categoria")
    # Redireciona para a lista de categorias
    return RedirectResponse(url="/categorias", status_code=303)

@app.get("/categorias/alterar/{id}")
async def alterar_categoria(request: Request, id: int):
    # Busca a categoria pelo ID
    categoria = categoria_repo.obter_categoria_por_id(id)
    # Se não encontrou a categoria, retorna erro 404
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    # Retorna a página de alteração de categoria com os dados da categoria
    return templates.TemplateResponse("alterar_categoria.html", {"request": request, "categoria": categoria})

@app.post("/categorias/alterar/{id}")
async def alterar_categoria_post(
    request: Request,
    id: int,
    nome: str = Form()
):
    # Se nome não for informado, retorna erro 400
    if not nome:
        raise HTTPException(status_code=400, detail="Nome é obrigatório")
    # Cria um objeto Categoria com os dados informados
    categoria = Categoria(id, nome)
    # Tenta atualizar a categoria no repositório
    if not categoria_repo.atualizar_categoria(categoria):
        raise HTTPException(status_code=400, detail="Erro ao atualizar categoria")
    # Redireciona para a lista de categorias
    return RedirectResponse(url="/categorias", status_code=303)

@app.get("/categorias/excluir/{id}")
async def excluir_categoria(request: Request, id: int):
    # Busca a categoria pelo ID
    categoria = categoria_repo.obter_categoria_por_id(id)
    # Se não encontrou a categoria, retorna erro 404
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    # Retorna a página de confirmação de exclusão de categoria
    if not categoria_repo.excluir_categoria(id):
        raise HTTPException(status_code=400, detail="Erro ao excluir categoria")
    # Redireciona para a lista de categorias
    return RedirectResponse(url="/categorias", status_code=303)

if __name__ == "__main__":
    uvicorn.run(app=app, port=8000, reload=True)