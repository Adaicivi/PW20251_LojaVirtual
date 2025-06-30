# Loja Virtual - E-commerce com FastAPI

## 🛠️ Tutoriais Úteis

[Tutorial: FastAPI com Jinja2](FASTAPI_JINJA.md)

[Tutorial: Testes com Pytest](TESTES_PYTEST.md)

## 📋 Visão Geral

Sistema de e-commerce desenvolvido em Python com FastAPI, oferecendo funcionalidades completas para gerenciamento de produtos, categorias, usuários e endereços. A aplicação implementa autenticação de usuários, diferentes níveis de acesso (usuário comum e administrador) e interface web responsiva.

## 🚀 Funcionalidades Principais

- **Gestão de Produtos**: Cadastro, listagem e visualização detalhada de produtos
- **Categorização**: Organização de produtos por categorias
- **Sistema de Usuários**: Cadastro, login e perfis de usuário
- **Níveis de Acesso**: Usuários comuns e administradores
- **Gestão de Endereços**: Múltiplos endereços por usuário
- **Interface Responsiva**: Design adaptável para diferentes dispositivos
- **Sistema de Paginação**: Para listas de produtos, usuários e categorias

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **FastAPI**: Framework web moderno e rápido
- **SQLite**: Banco de dados relacional leve
- **Jinja2**: Engine de templates HTML
- **Bootstrap 5**: Framework CSS para interface responsiva
- **Pytest**: Framework de testes
- **Babel**: Formatação de valores monetários

## 📦 Requisitos

### Dependências Principais
```
fastapi[standard]
uvicorn[standard]
jinja2
Babel
python-multipart
itsdangerous
```

### Dependências de Desenvolvimento
```
pytest
pytest-asyncio
pytest-cov
```

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd loja-virtual
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Como Executar

### Modo Desenvolvimento
```bash
python main.py
```
ou
```bash
uvicorn main:app --reload --port 8000
```

A aplicação estará disponível em: `http://localhost:8000`

### Executar Testes
```bash
# Todos os testes com cobertura
pytest

# Testes específicos
pytest tests/test_categoria_repo.py

# Testes sem cobertura
pytest --no-cov
```

## 📁 Estrutura do Projeto

```
loja-virtual/
├── main.py                 # Aplicação principal FastAPI
├── requirements.txt        # Dependências do projeto
├── pytest.ini             # Configuração dos testes
├── dados.db               # Banco de dados SQLite
├── .coveragerc            # Configuração de cobertura de testes
│
├── models/                # Modelos de dados
│   ├── categoria.py       # Modelo de categoria
│   ├── produto.py         # Modelo de produto
│   ├── usuario.py         # Modelo de usuário
│   └── endereco.py        # Modelo de endereço
│
├── repo/                  # Camada de repositório (acesso a dados)
│   ├── categoria_repo.py  # Repositório de categorias
│   ├── produto_repo.py    # Repositório de produtos
│   ├── usuario_repo.py    # Repositório de usuários
│   └── endereco_repo.py   # Repositório de endereços
│
├── sql/                   # Queries SQL
│   ├── categoria_sql.py   # SQL para categorias
│   ├── produto_sql.py     # SQL para produtos
│   ├── usuario_sql.py     # SQL para usuários
│   └── endereco_sql.py    # SQL para endereços
│
├── util/                  # Utilitários
│   ├── auth.py           # Autenticação e hash de senhas
│   ├── database.py       # Conexão com banco de dados
│   └── initializer.py    # Inicialização de tabelas e dados
│
├── templates/            # Templates HTML (Jinja2)
│   ├── base.html        # Template base
│   ├── index.html       # Página inicial
│   ├── produtos.html    # Lista de produtos
│   ├── produto.html     # Detalhe do produto
│   ├── categorias.html  # Lista de categorias
│   ├── usuarios.html    # Lista de usuários
│   ├── login.html       # Página de login
│   ├── cadastrar.html   # Cadastro de usuário
│   ├── perfil.html      # Perfil do usuário
│   └── ...              # Outros templates
│
├── data/                 # Dados iniciais SQL
│   ├── insert_usuarios.sql
│   ├── insert_produtos.sql
│   ├── insert_categorias.sql
│   └── insert_enderecos.sql
│
└── tests/               # Testes automatizados
    ├── conftest.py      # Fixtures dos testes
    ├── test_categoria_repo.py
    ├── test_produto_repo.py
    ├── test_usuario_repo.py
    └── test_endereco_repo.py
```

## 🌐 Endpoints da API

### Páginas Públicas
- `GET /` - Página inicial com produtos em destaque
- `GET /produtos/{id}` - Detalhes de um produto
- `GET /login` - Página de login
- `GET /cadastrar` - Página de cadastro

### Páginas Autenticadas
- `GET /perfil` - Perfil do usuário
- `GET /senha` - Alterar senha
- `GET /logout` - Encerrar sessão

### Páginas Administrativas
- `GET /usuarios` - Lista de usuários
- `GET /produtos` - Lista de produtos
- `GET /categorias` - Lista de categorias
- `GET /enderecos/{id_usuario}` - Endereços do usuário
- `GET /categorias/inserir` - Inserir categoria
- `GET /categorias/alterar/{id}` - Alterar categoria
- `GET /usuarios/promover/{id}` - Promover usuário
- `GET /usuarios/rebaixar/{id}` - Rebaixar usuário

### Operações POST
- `POST /login` - Autenticar usuário
- `POST /cadastrar` - Criar novo usuário
- `POST /perfil` - Atualizar perfil
- `POST /senha` - Atualizar senha
- `POST /categorias/inserir` - Criar categoria
- `POST /categorias/alterar/{id}` - Atualizar categoria

## 🏗️ Arquitetura

### Padrão Repository
A aplicação implementa o padrão Repository para separar a lógica de acesso a dados da lógica de negócios:

- **Models**: Classes de dados (dataclasses) que representam as entidades
- **Repositories**: Classes que encapsulam o acesso ao banco de dados
- **SQL**: Queries SQL separadas em módulos específicos
- **Main**: Controlador principal com as rotas FastAPI

### Autenticação
- Senhas armazenadas com hash SHA256
- Sessões gerenciadas via SessionMiddleware
- Dois tipos de usuário: 0 (comum) e 1 (administrador)

### Banco de Dados
- SQLite com foreign keys habilitadas
- Row factory configurado para retornar dicionários
- Dados iniciais carregados automaticamente

## 🧪 Testes

A aplicação possui cobertura completa de testes para a camada de repositório:

- Testes unitários para cada repositório
- Fixtures reutilizáveis em `conftest.py`
- Banco de dados temporário para testes
- Cobertura de código configurada

### Executar testes com relatório de cobertura:
```bash
pytest --cov=. --cov-report=html
```

O relatório HTML será gerado em `htmlcov/index.html`

## 👤 Usuário Padrão

Para testes, existe um usuário administrador padrão:
- **Email**: joaosilva@email.com
- **Senha**: 123456

## 🔐 Segurança

- Senhas armazenadas com hash SHA256
- Proteção contra SQL Injection via prepared statements
- Validação de sessão para áreas restritas
- Foreign keys para integridade referencial

## 📝 Notas de Desenvolvimento

- O arquivo `CLAUDE.md` contém instruções específicas para desenvolvimento com IA
- O banco de dados `dados.db` é criado automaticamente na primeira execução
- Os dados iniciais são carregados apenas se as tabelas estiverem vazias
- A configuração de testes usa bancos temporários para isolamento

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Autor

Desenvolvido por Ricardo Maroquio