# Tutorial Completo: FastAPI e Jinja2

## 1. Funcionamento das Aplicações Web

### 1.1 Conceitos Fundamentais

As aplicações web são construídas sobre o protocolo HTTP (Hypertext Transfer Protocol), que é o protocolo fundamental para troca de dados na Web. HTTP é um protocolo cliente-servidor, onde as requisições são iniciadas pelo cliente (geralmente um navegador web) e o servidor responde com os recursos solicitados.

### 1.2 Aplicações Estáticas vs Dinâmicas

**Aplicações Estáticas:**
- Servem conteúdo fixo (HTML, CSS, JavaScript)
- O conteúdo não muda com base na requisição
- Exemplo: um site institucional com páginas fixas

**Aplicações Dinâmicas:**
- Geram conteúdo em tempo real
- Respondem diferentemente baseado em dados, usuário, tempo, etc.
- Exemplo: o projeto Loja Virtual do codebase, que exibe produtos do banco de dados

### 1.3 O Protocolo HTTP

HTTP funciona através de um ciclo de requisição-resposta. O cliente envia uma requisição HTTP que contém métodos, cabeçalhos, corpo, etc., e quando o servidor recebe essa requisição, ele responde com uma resposta HTTP que contém status, cabeçalhos, corpo, etc.

#### Métodos HTTP Principais:
- **GET**: Recuperar dados (usado em `@app.get("/produtos")` no projeto)
- **POST**: Enviar dados (usado em `@app.post("/cadastrar")` no projeto)
- **PUT**: Atualizar dados existentes
- **DELETE**: Remover dados

#### Códigos de Status HTTP:
- **2xx**: Sucesso (200 OK, 201 Created)
- **3xx**: Redirecionamento (301 Moved Permanently, 303 See Other)
- **4xx**: Erro do cliente (400 Bad Request, 404 Not Found)
- **5xx**: Erro do servidor (500 Internal Server Error)

### 1.4 DNS e URLs

O DNS (Domain Name System) traduz nomes de domínio legíveis (como `lojavirtual.com`) em endereços IP. Uma URL completa tem a estrutura:

```
https://lojavirtual.com:8000/produtos/1?categoria=notebooks
  |        |              |      |     |        |
protocolo  domínio      porta  rota  param   query
```

## 2. FastAPI

### 2.1 Introdução ao FastAPI

FastAPI é um framework web moderno, de alta performance, fácil de aprender, rápido para codificar e pronto para produção. É baseado em Python 3.6+ e usa type hints padrão do Python.

### 2.2 Instalação e Configuração

```bash
pip install fastapi uvicorn[standard]
```

### 2.3 Estrutura Básica

Veja como o projeto Loja Virtual implementa uma aplicação FastAPI:

```python
from fastapi import FastAPI

# Cria a instância do FastAPI
app = FastAPI()

# Define uma rota básica
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à Loja Virtual"}
```

### 2.4 Rotas (Endpoints)

#### Rotas GET
No projeto, vemos várias rotas GET para exibir dados:

```python
@app.get("/produtos")
def read_produtos(request: Request):
    # Obtém os primeiros 12 produtos do banco de dados
    produtos = produto_repo.obter_produtos_por_pagina(1, 12)
    # Retorna os produtos (pode ser JSON ou HTML)
    return produtos
```

#### Rotas POST
Para receber dados de formulários:

```python
@app.post("/cadastrar")
async def cadastrar_usuario(
    request: Request,
    nome: str = Form(),
    email: str = Form(),
    senha: str = Form()
):
    # Processa os dados do formulário
    usuario = Usuario(nome=nome, email=email, senha_hash=hash_senha(senha))
    usuario_repo.inserir_usuario(usuario)
    return RedirectResponse(url="/login", status_code=303)
```

### 2.5 Parâmetros em Rotas

#### Path Parameters
Capturados diretamente da URL:

```python
@app.get("/produtos/{id}")
def read_produto(request: Request, id: int):
    produto = produto_repo.obter_produto_por_id(id)
    return produto
```

#### Query Parameters
Opcionais, vêm após `?` na URL:

```python
@app.get("/buscar")
def buscar_produtos(q: str = None, categoria: int = None):
    # URL: /buscar?q=notebook&categoria=1
    if q:
        produtos = produto_repo.buscar_por_nome(q)
    return produtos
```

### 2.6 Recebimento de Dados

#### Form Data
Para receber dados de formulários HTML, use `Form()` do FastAPI:

```python
from fastapi import Form

@app.post("/login")
async def login(
    email: str = Form(), 
    senha: str = Form()
):
    usuario = autenticar_usuario(email, senha)
    if usuario:
        return {"status": "success"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")
```

### 2.7 Tipos de Response

#### JSON Response (padrão)
```python
@app.get("/api/produtos")
def get_produtos():
    return {"produtos": [...]}  # Automaticamente convertido para JSON
```

#### HTML Response
```python
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Bem-vindo à Loja Virtual</h1>"
```

#### Redirect Response
```python
from fastapi.responses import RedirectResponse

@app.post("/logout")
def logout():
    return RedirectResponse(url="/", status_code=303)
```

### 2.8 Middleware e Sessões

O projeto usa SessionMiddleware para gerenciar sessões de usuário:

```python
from starlette.middleware.sessions import SessionMiddleware

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Usando sessões
@app.post("/login")
async def login(request: Request):
    # Armazena dados na sessão
    request.session["usuario"] = {"id": 1, "nome": "João"}
    
# Acessando dados da sessão
@app.get("/perfil")
def perfil(request: Request):
    usuario = request.session.get("usuario")
    if not usuario:
        raise HTTPException(status_code=401)
```

## 3. Jinja2

### 3.1 Introdução ao Jinja2

Jinja é um mecanismo de template rápido, expressivo e extensível. Placeholders especiais no template permitem escrever código similar à sintaxe Python. O template então recebe dados para renderizar o documento final.

### 3.2 Sintaxe Básica

#### Delimitadores do Jinja2

```jinja
{{ ... }}  {# Expressões (imprimir variáveis) #}
{% ... %}  {# Statements (lógica, loops) #}
{# ... #}  {# Comentários #}
```

### 3.3 Exibição de Objetos

No template `produto.html` do projeto:

```html
<h2>{{ produto.nome }}</h2>
<p>{{ produto.descricao }}</p>
<p>
    <strong class="text-danger fs-3">
        {{ produto.preco|format_currency_br }}
    </strong>
</p>
```

### 3.4 Criação de Variáveis

```jinja
{% set usuario = request.session["usuario"] or None %}
{% set titulo_pagina = "Detalhes do Produto" %}
```

### 3.5 Templates Base e Herança

#### Template Base (`base.html`)
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <title>{% block titulo %}Loja Virtual{% endblock %}</title>
</head>
<body>
    <header>
        <!-- Navegação comum -->
    </header>
    
    <main>
        {% block conteudo %}
        <!-- Conteúdo específico de cada página -->
        {% endblock %}
    </main>
    
    <footer>
        <!-- Rodapé comum -->
    </footer>
</body>
</html>
```

#### Template Filho (`produtos.html`)
```html
{% extends "base.html" %}

{% block titulo %}Nossos Produtos{% endblock %}

{% block conteudo %}
<h1>Produtos em Destaque</h1>
<div class="produtos">
    <!-- Conteúdo específico -->
</div>
{% endblock %}
```

### 3.6 Include para Componentes

```html
<!-- navbar.html -->
<nav class="navbar">
    <a href="/">Home</a>
    <a href="/produtos">Produtos</a>
</nav>

<!-- base.html -->
<body>
    {% include "components/navbar.html" %}
    {% block conteudo %}{% endblock %}
</body>
```

### 3.7 Estruturas de Controle

#### Condicionais
```jinja
{% if usuario %}
    <p>Olá, {{ usuario.nome }}!</p>
    {% if usuario.tipo == "admin" %}
        <a href="/admin">Painel Admin</a>
    {% endif %}
{% else %}
    <a href="/login">Faça Login</a>
{% endif %}
```

#### Loops
Do template `index.html` do projeto:

```jinja
<div class="row">
    {% for p in produtos %}
    <div class="col">
        <div class="card">
            <img src="{{ p.imagem }}" alt="{{ p.nome }}">
            <div class="card-body">
                <h6>{{ p.nome }}</h6>
                <p>{{ p.descricao }}</p>
                <strong>{{ p.preco|format_currency_br }}</strong>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
```

### 3.8 Filtros

Filtros em Jinja2 são usados para modificar dados que são fornecidos como variáveis. A sintaxe usa o pipe `|` para aplicar filtros.

#### Filtros Nativos
```jinja
{{ nome|upper }}           {# CONVERTE PARA MAIÚSCULAS #}
{{ nome|lower }}           {# converte para minúsculas #}
{{ nome|title }}           {# Primeira Letra Maiúscula #}
{{ texto|length }}         {# comprimento do texto #}
{{ lista|join(', ') }}     {# une elementos da lista #}
{{ numero|round(2) }}      {# arredonda para 2 casas #}
```

#### Filtros Customizados
O projeto define um filtro para formatar moeda brasileira:

```python
def format_currency_br(value, currency='BRL', locale='pt_BR'):
    return format_currency(value, currency, locale=locale)

# Registra o filtro
templates.env.filters['format_currency_br'] = format_currency_br
```

Uso no template:
```jinja
{{ produto.preco|format_currency_br }}  {# R$ 199,90 #}
```

## 4. Usando Jinja2 com FastAPI

### 4.1 Configuração Inicial

Para usar Jinja2 com FastAPI, você precisa importar Jinja2Templates e criar um objeto templates que pode ser reutilizado. Declare um parâmetro Request na operação de rota que retornará um template.

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Configura templates
templates = Jinja2Templates(directory="templates")

# Configura arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
```

### 4.2 Renderizando Templates

```python
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    produtos = produto_repo.obter_produtos_por_pagina(1, 12)
    
    return templates.TemplateResponse(
        "index.html",  # nome do template
        {
            "request": request,  # sempre necessário
            "produtos": produtos,  # dados para o template
            "titulo": "Produtos em Destaque"
        }
    )
```

### 4.3 Apresentação de Coleções

No projeto, a listagem de produtos demonstra como apresentar coleções:

```python
# main.py
@app.get("/produtos")
def read_produtos(request: Request):
    produtos = produto_repo.obter_produtos_por_pagina(1, 12)
    return templates.TemplateResponse(
        "produtos.html", 
        {"request": request, "produtos": produtos}
    )
```

```html
<!-- produtos.html -->
<table class="table">
    <thead>
        <tr>
            <th>Nome</th>
            <th>Preço</th>
            <th>Estoque</th>
        </tr>
    </thead>
    <tbody>
        {% for produto in produtos %}
        <tr>
            <td>{{ produto.nome }}</td>
            <td>{{ produto.preco|format_currency_br }}</td>
            <td>{{ produto.estoque }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

### 4.4 Processamento de Formulários

#### Template do Formulário
```html
<!-- cadastrar.html -->
<form method="post" action="/cadastrar">
    <div class="form-floating mb-3">
        <input type="text" class="form-control" 
               id="nome" name="nome" required>
        <label for="nome">Nome</label>
    </div>
    
    <div class="form-floating mb-3">
        <input type="email" class="form-control" 
               id="email" name="email" required>
        <label for="email">E-mail</label>
    </div>
    
    <button type="submit" class="btn btn-primary">
        Cadastrar
    </button>
</form>
```

#### Processamento no FastAPI
```python
@app.get("/cadastrar")
def form_cadastro(request: Request):
    return templates.TemplateResponse(
        "cadastrar.html", 
        {"request": request}
    )

@app.post("/cadastrar")
async def processar_cadastro(
    request: Request,
    nome: str = Form(),
    email: str = Form(),
    senha: str = Form()
):
    try:
        # Processa o cadastro
        usuario = Usuario(nome=nome, email=email, senha_hash=hash_senha(senha))
        usuario_repo.inserir_usuario(usuario)
        
        # Redireciona para login
        return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        # Em caso de erro, retorna ao formulário com mensagem
        return templates.TemplateResponse(
            "cadastrar.html",
            {
                "request": request,
                "erro": "Erro ao cadastrar usuário",
                "nome": nome,
                "email": email
            }
        )
```

### 4.5 Upload de Imagens

```python
from fastapi import UploadFile, File
import shutil
from pathlib import Path

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload-produto")
async def upload_imagem_produto(
    request: Request,
    imagem: UploadFile = File(...),
    nome: str = Form(),
    preco: float = Form()
):
    # Salva a imagem
    file_path = UPLOAD_DIR / imagem.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(imagem.file, buffer)
    
    # Salva o produto com o caminho da imagem
    produto = Produto(
        nome=nome,
        preco=preco,
        imagem=f"/static/uploads/{imagem.filename}"
    )
    produto_repo.inserir_produto(produto)
    
    return RedirectResponse(url="/produtos", status_code=303)
```

### 4.6 AJAX e Atualizações Dinâmicas

Para atualizações sem recarregar a página:

```html
<!-- Template com JavaScript -->
<div id="produtos-lista">
    {% for produto in produtos %}
        <div class="produto-item">{{ produto.nome }}</div>
    {% endfor %}
</div>

<button onclick="carregarMaisProdutos()">Carregar Mais</button>

<script>
async function carregarMaisProdutos() {
    const response = await fetch('/api/produtos?pagina=2');
    const data = await response.json();
    
    const lista = document.getElementById('produtos-lista');
    data.produtos.forEach(produto => {
        const div = document.createElement('div');
        div.className = 'produto-item';
        div.textContent = produto.nome;
        lista.appendChild(div);
    });
}
</script>
```

```python
# Endpoint da API
@app.get("/api/produtos")
def api_produtos(pagina: int = 1):
    produtos = produto_repo.obter_produtos_por_pagina(pagina, 12)
    return {"produtos": produtos}
```

### 4.7 Validação e Mensagens de Erro

```python
@app.post("/login")
async def login(request: Request, email: str = Form(), senha: str = Form()):
    usuario = autenticar_usuario(email, senha)
    
    if not usuario:
        # Retorna ao formulário com erro
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "erro": "Email ou senha incorretos",
                "email": email  # Preserva o email digitado
            }
        )
    
    # Login bem-sucedido
    request.session["usuario"] = {"id": usuario.id, "nome": usuario.nome}
    return RedirectResponse(url="/", status_code=303)
```

```html
<!-- login.html -->
{% if erro %}
<div class="alert alert-danger">{{ erro }}</div>
{% endif %}

<form method="post">
    <input type="email" name="email" 
           value="{{ email or '' }}" required>
    <input type="password" name="senha" required>
    <button type="submit">Entrar</button>
</form>
```

### 4.8 Paginação

Implementando paginação com Jinja2 e FastAPI:

```python
@app.get("/produtos")
def listar_produtos(request: Request, pagina: int = 1):
    por_pagina = 12
    produtos = produto_repo.obter_produtos_por_pagina(pagina, por_pagina)
    total = produto_repo.contar_total_produtos()
    total_paginas = (total + por_pagina - 1) // por_pagina
    
    return templates.TemplateResponse(
        "produtos.html",
        {
            "request": request,
            "produtos": produtos,
            "pagina_atual": pagina,
            "total_paginas": total_paginas
        }
    )
```

```html
<!-- produtos.html -->
<nav>
    <ul class="pagination">
        {% if pagina_atual > 1 %}
        <li class="page-item">
            <a class="page-link" href="/produtos?pagina={{ pagina_atual - 1 }}">
                Anterior
            </a>
        </li>
        {% endif %}
        
        {% for p in range(1, total_paginas + 1) %}
        <li class="page-item {% if p == pagina_atual %}active{% endif %}">
            <a class="page-link" href="/produtos?pagina={{ p }}">{{ p }}</a>
        </li>
        {% endfor %}
        
        {% if pagina_atual < total_paginas %}
        <li class="page-item">
            <a class="page-link" href="/produtos?pagina={{ pagina_atual + 1 }}">
                Próxima
            </a>
        </li>
        {% endif %}
    </ul>
</nav>
```

## Boas Práticas

### 1. Organização de Templates
```
templates/
├── base/
│   └── base.html
├── components/
│   ├── navbar.html
│   ├── footer.html
│   └── forms/
│       └── produto_form.html
├── pages/
│   ├── home.html
│   ├── produtos.html
│   └── admin/
│       └── dashboard.html
└── errors/
    ├── 404.html
    └── 500.html
```

### 2. Contexto Global
```python
# Adiciona variáveis globais aos templates
@app.middleware("http")
async def add_global_context(request: Request, call_next):
    response = await call_next(request)
    return response

# Ou use um processador de contexto
def get_common_context(request: Request):
    return {
        "request": request,
        "usuario": request.session.get("usuario"),
        "ano_atual": datetime.now().year,
        "nome_site": "Loja Virtual"
    }
```

### 3. Cache de Templates
```python
# Em produção, desabilite auto-reload
templates = Jinja2Templates(
    directory="templates",
    auto_reload=False  # Melhora performance
)
```

### 4. Segurança
- Sempre escape conteúdo do usuário (Jinja2 faz isso por padrão)
- Use `|safe` apenas quando tiver certeza absoluta
- Valide todos os dados de entrada no FastAPI
- Use HTTPS em produção

## Conclusão

FastAPI e Jinja2 formam uma combinação poderosa para criar aplicações web dinâmicas em Python. O FastAPI fornece um backend rápido e moderno com validação automática, enquanto o Jinja2 oferece um sistema de templates flexível e poderoso.

O projeto Loja Virtual demonstra na prática como essas tecnologias trabalham juntas para criar uma aplicação completa, desde a renderização de páginas até o processamento de formulários e gerenciamento de sessões.

### Próximos Passos
1. Explore recursos avançados do FastAPI como WebSockets e background tasks
2. Aprenda sobre macros e filtros customizados no Jinja2
3. Implemente autenticação JWT para APIs
4. Adicione testes automatizados com pytest
5. Configure deployment com Docker e CI/CD