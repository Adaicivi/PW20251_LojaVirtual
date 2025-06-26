# Tutorial Completo: Testes com pytest

## Introdução: Por que Testar?

Testes automatizados são fundamentais para garantir que seu código funcione corretamente e continue funcionando após mudanças. Eles ajudam a:

- Detectar bugs antes que cheguem à produção
- Facilitar refatorações com segurança
- Documentar o comportamento esperado do código
- Economizar tempo a longo prazo

## 1. Conceitos Fundamentais de Testes

### 1.1 O que são Testes Unitários?

Testes unitários verificam o comportamento de pequenas unidades de código (funções, métodos, classes) de forma isolada. No projeto Loja Virtual, vemos testes para cada repositório:

```python
# Testa uma única função do repositório
def test_inserir_categoria(self, test_db, categoria_exemplo):
    categoria_repo.criar_tabela_categorias()
    id_categoria_inserida = categoria_repo.inserir_categoria(categoria_exemplo)
    
    # Verifica se a inserção funcionou
    categoria_db = categoria_repo.obter_categoria_por_id(id_categoria_inserida)
    assert categoria_db is not None
```

### 1.2 Padrão AAA (Arrange, Act, Assert)

A maioria dos testes segue o padrão AAA:

```python
def test_atualizar_categoria_existente(self, test_db, categoria_exemplo):
    # Arrange - Prepara os dados necessários
    categoria_repo.criar_tabela_categorias()
    id_categoria_inserida = categoria_repo.inserir_categoria(categoria_exemplo)
    categoria_inserida = categoria_repo.obter_categoria_por_id(id_categoria_inserida)
    
    # Act - Executa a ação sendo testada
    categoria_inserida.nome = "Categoria Atualizada"
    resultado = categoria_repo.atualizar_categoria(categoria_inserida)
    
    # Assert - Verifica o resultado
    assert resultado == True
    categoria_db = categoria_repo.obter_categoria_por_id(id_categoria_inserida)
    assert categoria_db.nome == "Categoria Atualizada"
```

## 2. Instalação e Configuração do pytest

### 2.1 Instalação

pytest requer Python 3.8+ ou PyPy3 e pode ser instalado usando pip:

```bash
pip install pytest pytest-cov
```

### 2.2 Estrutura de Diretórios

O projeto Loja Virtual segue a estrutura recomendada:

```
projeto/
├── main.py
├── models/
├── repo/
├── tests/              # Diretório de testes
│   ├── __init__.py
│   ├── conftest.py     # Configurações e fixtures globais
│   ├── test_categoria_repo.py
│   ├── test_produto_repo.py
│   └── test_usuario_repo.py
└── pytest.ini          # Configuração do pytest
```

### 2.3 Arquivo pytest.ini

O arquivo `pytest.ini` configura o comportamento do pytest:

```ini
[tool:pytest]
# Diretórios onde o pytest deve procurar por testes
testpaths = tests

# Padrões de arquivos de teste
python_files = test_*.py *_test.py

# Padrões de classes de teste
python_classes = Test*

# Padrões de funções de teste
python_functions = test_*

# Marcadores personalizados
markers =
    slow: marca testes que demoram para executar
    integration: marca testes de integração
    unit: marca testes unitários

# Opções padrão do pytest COM coverage
addopts = 
    -v                          # Verbose
    --strict-markers           # Força uso de marcadores registrados
    --disable-warnings         # Desabilita avisos
    --color=yes               # Saída colorida
    --tb=short                # Traceback curto
    --maxfail=1               # Para após 1 falha
    --cov=.                   # Coverage do projeto
    --cov-report=html         # Relatório HTML
    --cov-report=term-missing # Relatório no terminal
```

## 3. Escrevendo Testes Básicos

### 3.1 Nomenclatura e Descoberta de Testes

O pytest framework torna fácil escrever testes pequenos e legíveis. pytest descobre automaticamente testes seguindo convenções:

- Arquivos: `test_*.py` ou `*_test.py`
- Classes: começando com `Test`
- Funções: começando com `test_`

### 3.2 Assertions Simples

pytest usa a declaração `assert` padrão do Python:

```python
def test_criar_tabela_categorias(self, test_db):
    # Act
    resultado = categoria_repo.criar_tabela_categorias()
    
    # Assert
    assert resultado == True, "A criação da tabela deveria retornar True"
```

### 3.3 Testando Exceções

```python
def test_excluir_categoria_inexistente(self, test_db):
    categoria_repo.criar_tabela_categorias()
    
    # Tenta excluir categoria que não existe
    resultado = categoria_repo.excluir_categoria(999)
    
    # Verifica se retornou False (falha esperada)
    assert resultado == False
```

## 4. Fixtures: O Poder do pytest

### 4.1 O que são Fixtures?

Fixtures são funções que você define para servir como setup dos testes. No pytest, "fixtures" são funções decoradas com @pytest.fixture que fornecem dados ou estado necessários para os testes.

### 4.2 Fixtures Básicas

No arquivo `conftest.py` do projeto:

```python
import pytest

@pytest.fixture
def categoria_exemplo():
    # Cria uma categoria de exemplo para os testes
    from models.categoria import Categoria
    categoria = Categoria(0, "Categoria Teste")
    return categoria

@pytest.fixture
def produto_exemplo():
    # Cria um produto de exemplo para os testes
    from models.produto import Produto
    produto = Produto(
        id=0,
        nome="Produto Teste",
        descricao="Descrição do produto teste.",
        preco=10.0,
        estoque=5,
        imagem="produto.jpg",
        id_categoria=1
    )
    return produto
```

### 4.3 Usando Fixtures em Testes

Testes solicitam fixtures declarando-as como argumentos:

```python
def test_inserir_produto(self, test_db, categoria_exemplo, produto_exemplo):
    # As fixtures são automaticamente injetadas
    categoria_repo.criar_tabela_categorias()
    categoria_repo.inserir_categoria(categoria_exemplo)
    produto_repo.criar_tabela_produtos()
    
    # Usa o produto_exemplo fornecido pela fixture
    id_produto_inserido = produto_repo.inserir_produto(produto_exemplo)
    
    assert id_produto_inserido is not None
```

### 4.4 Fixtures com Setup e Teardown

A fixture `test_db` do projeto demonstra setup/teardown:

```python
@pytest.fixture
def test_db():
    # Setup: Cria um arquivo temporário para o banco de dados
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['TEST_DATABASE_PATH'] = db_path
    
    # Retorna o caminho do banco temporário
    yield db_path
    
    # Teardown: Remove o arquivo após o teste
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)
```

### 4.5 Fixtures que Usam Outras Fixtures

Fixtures podem usar outras fixtures, criando uma cadeia de dependências:

```python
@pytest.fixture
def usuario_com_endereco(usuario_exemplo, endereco_exemplo):
    # usuario_exemplo e endereco_exemplo são outras fixtures
    usuario_repo.criar_tabela_usuarios()
    endereco_repo.criar_tabela_enderecos()
    
    # Insere usuário
    id_usuario = usuario_repo.inserir_usuario(usuario_exemplo)
    
    # Associa endereço ao usuário
    endereco_exemplo.id_usuario = id_usuario
    endereco_repo.inserir_endereco(endereco_exemplo)
    
    return usuario_repo.obter_usuario_por_id(id_usuario)
```

### 4.6 Escopo de Fixtures

Fixtures são criadas quando primeiro requisitadas por um teste e destruídas baseadas em seu escopo:

```python
@pytest.fixture(scope="function")  # Padrão - nova instância para cada teste
def conexao_db():
    return obter_conexao()

@pytest.fixture(scope="class")     # Uma instância por classe de teste
def config_classe():
    return {"timeout": 30}

@pytest.fixture(scope="module")    # Uma instância por módulo
def dados_compartilhados():
    return carregar_dados_teste()

@pytest.fixture(scope="session")   # Uma instância para toda sessão de teste
def servidor_teste():
    servidor = iniciar_servidor()
    yield servidor
    servidor.parar()
```

## 5. Organizando Testes em Classes

O projeto organiza testes em classes para melhor estrutura:

```python
class TestCategoriaRepo:
    """Agrupa todos os testes do repositório de categorias"""
    
    def test_criar_tabela_categorias(self, test_db):
        resultado = categoria_repo.criar_tabela_categorias()
        assert resultado == True
    
    def test_inserir_categoria(self, test_db, categoria_exemplo):
        categoria_repo.criar_tabela_categorias()
        id_categoria = categoria_repo.inserir_categoria(categoria_exemplo)
        assert id_categoria is not None
    
    def test_obter_categoria_por_id_existente(self, test_db, categoria_exemplo):
        # ... mais testes relacionados
```

## 6. Testes Parametrizados

### 6.1 Parametrização Básica

@pytest.mark.parametrize permite definir múltiplos conjuntos de argumentos e fixtures no nível da função ou classe de teste:

```python
import pytest

@pytest.mark.parametrize("nome_categoria,esperado_valido", [
    ("Eletrônicos", True),
    ("", False),              # Nome vazio
    (None, False),            # Nome nulo
    ("A" * 256, False),       # Nome muito longo
])
def test_validar_nome_categoria(nome_categoria, esperado_valido):
    resultado = validar_nome_categoria(nome_categoria)
    assert resultado == esperado_valido
```

### 6.2 Parametrização com Fixtures

```python
@pytest.fixture
def lista_categorias_exemplo():
    from models.categoria import Categoria
    return [
        Categoria(0, f"Categoria {i:02d}")
        for i in range(1, 11)
    ]

@pytest.mark.parametrize("pagina,tamanho,esperado", [
    (1, 4, 4),   # Primeira página, 4 itens
    (2, 4, 4),   # Segunda página, 4 itens
    (3, 4, 2),   # Terceira página, 2 itens restantes
    (4, 4, 0),   # Quarta página, vazia
])
def test_obter_categorias_paginadas(test_db, lista_categorias_exemplo, 
                                   pagina, tamanho, esperado):
    # Insere todas as categorias
    categoria_repo.criar_tabela_categorias()
    for cat in lista_categorias_exemplo:
        categoria_repo.inserir_categoria(cat)
    
    # Testa paginação
    resultado = categoria_repo.obter_categorias_por_pagina(pagina, tamanho)
    assert len(resultado) == esperado
```

## 7. Testando com Banco de Dados

### 7.1 Isolamento de Testes

O projeto usa um banco de dados temporário para cada teste:

```python
def test_inserir_usuario(self, test_db, usuario_exemplo):
    # test_db garante um banco limpo e isolado
    usuario_repo.criar_tabela_usuarios()
    
    # Testa inserção
    id_usuario = usuario_repo.inserir_usuario(usuario_exemplo)
    
    # Verifica se foi inserido
    usuario_db = usuario_repo.obter_usuario_por_id(id_usuario)
    assert usuario_db is not None
    assert usuario_db.nome == usuario_exemplo.nome
```

### 7.2 Testando Relacionamentos

```python
def test_obter_enderecos_por_usuario(self, test_db, endereco_exemplo, usuario_exemplo):
    # Prepara o banco com as tabelas necessárias
    usuario_repo.criar_tabela_usuarios()
    id_usuario = usuario_repo.inserir_usuario(usuario_exemplo)
    endereco_repo.criar_tabela_enderecos()
    
    # Insere 3 endereços para o usuário
    for i in range(3):
        endereco_exemplo.id_usuario = id_usuario
        endereco_exemplo.logradouro = f"Rua {i+1}"
        endereco_repo.inserir_endereco(endereco_exemplo)
    
    # Testa a busca
    enderecos = endereco_repo.obter_enderecos_por_usuario(id_usuario)
    
    # Verifica
    assert len(enderecos) == 3
    assert all(e.id_usuario == id_usuario for e in enderecos)
```

## 8. Coverage (Cobertura de Testes)

### 8.1 Configuração

O arquivo `.coveragerc` configura a análise de cobertura:

```ini
[run]
source = .
omit = 
    */.venv/*
    */tests/*
    */test_*
    setup.py
    main.py
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstract

[html]
directory = htmlcov
```

### 8.2 Executando com Coverage

```bash
# Executa testes com coverage
pytest

# Gera relatório HTML detalhado
pytest --cov-report=html

# Visualiza coverage no terminal
pytest --cov-report=term-missing
```

## 9. Marcadores (Markers)

### 9.1 Definindo Marcadores

```python
import pytest

@pytest.mark.slow
def test_operacao_demorada():
    # Teste que demora muito tempo
    processar_grande_volume_dados()

@pytest.mark.integration
def test_integracao_completa():
    # Teste que envolve múltiplos componentes
    resultado = sistema_completo()
    assert resultado.sucesso
```

### 9.2 Executando Testes por Marcador

```bash
# Executa apenas testes rápidos (pula os lentos)
pytest -m "not slow"

# Executa apenas testes de integração
pytest -m integration

# Executa testes unitários mas não de integração
pytest -m "unit and not integration"
```

## 10. Boas Práticas

### 10.1 Nomeação Clara

```python
# ❌ Ruim
def test_1():
    assert True

# ✅ Bom
def test_inserir_produto_com_dados_validos_retorna_id():
    # ...
```

### 10.2 Um Conceito por Teste

```python
# ❌ Ruim - testa múltiplas coisas
def test_produto():
    # Testa inserção
    id_produto = produto_repo.inserir_produto(produto)
    assert id_produto is not None
    
    # Testa atualização
    produto.nome = "Novo Nome"
    assert produto_repo.atualizar_produto(produto)
    
    # Testa exclusão
    assert produto_repo.excluir_produto(id_produto)

# ✅ Bom - testes separados
def test_inserir_produto_retorna_id_valido():
    id_produto = produto_repo.inserir_produto(produto)
    assert id_produto is not None

def test_atualizar_produto_existente_retorna_true():
    produto.nome = "Novo Nome"
    resultado = produto_repo.atualizar_produto(produto)
    assert resultado == True

def test_excluir_produto_existente_retorna_true():
    resultado = produto_repo.excluir_produto(id_produto)
    assert resultado == True
```

### 10.3 Mensagens de Erro Descritivas

```python
def test_obter_produtos_por_pagina_primeira_pagina(self, test_db, lista_produtos):
    produtos = produto_repo.obter_produtos_por_pagina(1, 4)
    
    assert len(produtos) == 4, "Deveria retornar 4 produtos na primeira página"
    
    ids_esperados = [1, 2, 3, 4]
    ids_retornados = [p.id for p in produtos]
    assert ids_retornados == ids_esperados, \
        f"IDs esperados: {ids_esperados}, mas obteve: {ids_retornados}"
```

### 10.4 Teste de Casos Extremos

```python
def test_obter_enderecos_usuario_sem_enderecos(self, test_db, usuario_exemplo):
    # Testa caso onde usuário não tem endereços
    usuario_repo.criar_tabela_usuarios()
    id_usuario = usuario_repo.inserir_usuario(usuario_exemplo)
    endereco_repo.criar_tabela_enderecos()
    
    # Busca endereços de usuário sem endereços
    enderecos = endereco_repo.obter_enderecos_por_usuario(id_usuario)
    
    assert isinstance(enderecos, list), "Deveria retornar uma lista"
    assert len(enderecos) == 0, "Lista deveria estar vazia"
```

## 11. Executando Testes

### 11.1 Comandos Básicos

```bash
# Executa todos os testes
pytest

# Executa com saída detalhada
pytest -v

# Executa arquivo específico
pytest tests/test_categoria_repo.py

# Executa teste específico
pytest tests/test_categoria_repo.py::TestCategoriaRepo::test_inserir_categoria

# Para após primeira falha
pytest -x

# Executa últimas falhas
pytest --lf
```

### 11.2 Filtros e Seleção

```bash
# Executa testes que contêm "categoria" no nome
pytest -k categoria

# Executa testes exceto os que contêm "slow"
pytest -k "not slow"

# Mostra quais testes seriam executados
pytest --collect-only
```

## 12. Debugging de Testes

### 12.1 Print Debugging

```python
def test_com_debug(self, test_db, produto_exemplo):
    print(f"Produto antes: {produto_exemplo}")  # Use -s para ver prints
    
    id_produto = produto_repo.inserir_produto(produto_exemplo)
    print(f"ID inserido: {id_produto}")
    
    produto_db = produto_repo.obter_produto_por_id(id_produto)
    print(f"Produto após: {produto_db}")
    
    assert produto_db is not None
```

Execute com `pytest -s` para ver os prints.

### 12.2 Usando pdb

```python
def test_com_breakpoint(self):
    resultado = funcao_complexa()
    
    # Para debugar quando resultado não é esperado
    if resultado != esperado:
        import pdb; pdb.set_trace()  # ou apenas breakpoint() no Python 3.7+
    
    assert resultado == esperado
```

## Conclusão

pytest é uma ferramenta poderosa que torna os testes em Python simples e eficientes. Com sua capacidade de escrever testes pequenos e legíveis que podem escalar para suportar testes funcionais complexos, pytest se tornou a escolha preferida para muitos projetos Python.

Os principais conceitos abordados:

1. **Estrutura básica**: Convenções de nomenclatura e organização
2. **Fixtures**: Sistema poderoso para gerenciar dependências de teste
3. **Assertions**: Uso de `assert` com mensagens descritivas
4. **Parametrização**: Executar o mesmo teste com diferentes dados
5. **Coverage**: Medir a cobertura de código dos testes
6. **Boas práticas**: Escrever testes claros e mantíveis

Com esses conhecimentos, você está pronto para criar testes semelhantes aos do projeto Loja Virtual, garantindo que seu código seja robusto e confiável.