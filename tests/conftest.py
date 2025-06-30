from datetime import datetime
import pytest
import os
import sys
import tempfile

# Adiciona o diretório raiz do projeto ao PYTHONPATH
# Isso permite importar módulos do projeto nos testes
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Fixture para criar um banco de dados temporário para testes
@pytest.fixture
def test_db():
    # Cria um arquivo temporário para o banco de dados
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    # Configura a variável de ambiente para usar o banco de teste
    os.environ['TEST_DATABASE_PATH'] = db_path
    # Retorna o caminho do banco de dados temporário
    yield db_path    
    # Remove o arquivo temporário ao concluir o teste
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def categoria_exemplo():
    # Cria uma categoria de exemplo para os testes
    from models.categoria import Categoria
    categoria = Categoria(0, "Categoria Teste")
    return categoria

@pytest.fixture
def lista_categorias_exemplo():
    # Cria uma lista de 10 categorias de exemplo para os testes
    from models.categoria import Categoria
    categorias = []
    for i in range(1, 11):
        categoria = Categoria(0, f"Categoria {i:02d}")
        categorias.append(categoria)
    return categorias

@pytest.fixture
def produto_exemplo():
    # Cria um produto de exemplo para os testes
    from models.produto import Produto
    produto = Produto(0, "Produto Teste", "Descrição do produto teste.", 10.0, 5, "produto.jpg", 1)
    return produto

@pytest.fixture
def lista_produtos_exemplo(categoria_exemplo):
    # Cria uma lista de 10 produtos de exemplo para os testes
    from models.produto import Produto
    produtos = []
    for i in range(1, 11):
        produto = Produto(0, f"Produto {i:02d}", f"Descrição do produto {i:02}.", 10.0*i, 5*i, f"produto{i}.jpg", i)
        produtos.append(produto)
    return produtos

@pytest.fixture
def usuario_exemplo():
    # Cria um usuário de exemplo para os testes
    from models.usuario import Usuario
    usuario = Usuario(0, "Usuário Teste", "123.456.789-00", "(28) 99999-0000", "usuario@email.com", datetime(2000, 1, 1).date(), "123456", 0)
    return usuario

@pytest.fixture
def lista_usuarios_exemplo():
    # Cria uma lista de 10 usuários de exemplo para os testes
    from models.usuario import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Usuário {i:02d}", f"123.456.789-{i:02d}", f"(28) 99999-00{i:02d}", f"usuario{i:02d}@email.com", datetime(2000, 1, i).date(), "123456", 0)
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def endereco_exemplo():
    # Cria um endereço de exemplo para os testes
    from models.endereco import Endereco
    endereco = Endereco(0, "Rua Teste", "123", "Casa", "Bairro Teste", "Cidade Teste", "Estado Teste", "12345-678", 1)
    return endereco

@pytest.fixture
def lista_enderecos_exemplo():
    # Cria uma lista de 10 endereços de exemplo para os testes
    from models.endereco import Endereco
    enderecos = []
    for i in range(1, 11):
        endereco = Endereco(0, f"Rua {i:02d}", f"{i*3}", f"Apto 2{i:02d}", f"Bairro {i:02d}", f"Cidade {i:02d}", f"Estado {i:02d}", f"12345-0{i:02d}", i)
        enderecos.append(endereco)
    return enderecos