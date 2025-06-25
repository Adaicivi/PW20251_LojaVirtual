import sys
import os

# Adiciona o diretório raiz do projeto ao path se necessário
if not any('projeto' in path for path in sys.path):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)

from models.produto import Produto
from repo import produto_repo

class TestProdutoRepo:
    def test_criar_tabela_produtos(self, test_db):
        # Arrange: prepara o banco de dados para criar a tabela
        # Act: chama o método para criar a tabela
        resultado = produto_repo.criar_tabela_produtos()
        # Assert: verifica se a tabela foi criada com sucesso
        assert resultado == True, "A tabela de produtos deveria ser criada com sucesso"
    
    def test_inserir_produto_sucesso(self, test_db, produto_exemplo):
        # Arrange: prepara o banco e cria a tabela
        produto_repo.criar_tabela_produtos()
        # Act: insere o produto de exemplo
        produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Assert: verifica se o produto foi inserido corretamente
        assert produto_inserido is not None, "O produto inserido não deveria ser None"
        assert produto_inserido.id > 0, "O produto inserido deveria ter um ID válido"
        assert produto_inserido.nome == produto_exemplo.nome, "O nome do produto não confere"
        assert produto_inserido.descricao == produto_exemplo.descricao, "A descrição não confere"
        assert produto_inserido.preco == produto_exemplo.preco, "O preço não confere"
        assert produto_inserido.estoque == produto_exemplo.estoque, "O estoque não confere"
        assert produto_inserido.imagem == produto_exemplo.imagem, "A imagem não confere"
    
    def test_obter_produto_por_id_existente(self, test_db, produto_exemplo):
        # Arrange: prepara o banco e insere um produto
        produto_repo.criar_tabela_produtos()
        produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Act: busca o produto pelo ID
        produto_encontrado = produto_repo.obter_produto_por_id(produto_inserido.id)
        # Assert: verifica se encontrou o produto correto
        assert produto_encontrado is not None, "Deveria encontrar o produto"
        assert produto_encontrado.id == produto_inserido.id, "O ID não confere"
        assert produto_encontrado.nome == produto_exemplo.nome, "O nome não confere"
    
    def test_obter_produto_por_id_inexistente(self, test_db):
        # Arrange: prepara o banco (sem inserir produtos)
        produto_repo.criar_tabela_produtos()
        # Act: tenta buscar um produto com ID que não existe
        produto_encontrado = produto_repo.obter_produto_por_id(999)
        # Assert: verifica se retorna None
        assert produto_encontrado is None, "Deveria retornar None para produto inexistente"
    
    def test_atualizar_produto_existente(self, test_db, produto_exemplo):
        # Arrange: insere um produto para depois atualizar
        produto_repo.criar_tabela_produtos()
        produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Modifica os dados do produto
        produto_inserido.nome = "Produto Atualizado"
        produto_inserido.preco = 199.99
        produto_inserido.estoque = 20
        # Act: atualiza o produto
        resultado = produto_repo.atualizar_produto(produto_inserido)
        # Assert: verifica se a atualização foi bem-sucedida
        assert resultado == True, "A atualização deveria retornar True"
        # Verifica se os dados foram realmente atualizados no banco
        produto_atualizado = produto_repo.obter_produto_por_id(produto_inserido.id)
        assert produto_atualizado.nome == "Produto Atualizado", "O nome não foi atualizado"
        assert produto_atualizado.preco == 199.99, "O preço não foi atualizado"
        assert produto_atualizado.estoque == 20, "O estoque não foi atualizado"
    
    def test_atualizar_produto_inexistente(self, test_db, produto_exemplo):
        # Arrange: prepara o banco sem inserir produtos
        produto_repo.criar_tabela_produtos()
        produto_exemplo.id = 999  # ID que não existe
        # Act: tenta atualizar um produto inexistente
        resultado = produto_repo.atualizar_produto(produto_exemplo)
        # Assert: verifica se retorna False
        assert resultado == False, "Deveria retornar False para produto inexistente"
    
    def test_excluir_produto_existente(self, test_db, produto_exemplo):
        # Arrange: insere um produto para depois excluir
        produto_repo.criar_tabela_produtos()
        produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Act: exclui o produto
        resultado = produto_repo.excluir_produto(produto_inserido.id)
        # Assert: verifica se a exclusão foi bem-sucedida
        assert resultado == True, "A exclusão deveria retornar True"
        # Verifica se o produto foi realmente excluído
        produto_excluido = produto_repo.obter_produto_por_id(produto_inserido.id)
        assert produto_excluido is None, "O produto deveria ter sido excluído"
    
    def test_excluir_produto_inexistente(self, test_db):
        # Arrange: prepara o banco sem produtos
        produto_repo.criar_tabela_produtos()
        # Act: tenta excluir um produto inexistente
        resultado = produto_repo.excluir_produto(999)
        # Assert: verifica se retorna False
        assert resultado == False, "Deveria retornar False para produto inexistente"
    
    def test_obter_produtos_por_pagina_primeira_pagina(self, test_db, lista_produtos_exemplo):
        # Arrange: insere vários produtos
        produto_repo.criar_tabela_produtos()
        for produto in lista_produtos_exemplo:
            produto_repo.inserir_produto(produto)
        # Act: busca a primeira página com 3 produtos por página
        produtos_pagina = produto_repo.obter_produtos_por_pagina(numero_pagina=1, tamanho_pagina=3)
        # Assert: verifica se retornou a quantidade correta
        assert len(produtos_pagina) == 3, "Deveria retornar 3 produtos na primeira página"
        # Verifica se os produtos estão ordenados por nome (conforme SQL)
        nomes_esperados = ["Produto A", "Produto B", "Produto C"]
        nomes_retornados = [p.nome for p in produtos_pagina]
        assert nomes_retornados == nomes_esperados, "Os produtos não estão na ordem correta"
    
    def test_obter_produtos_por_pagina_segunda_pagina(self, test_db, lista_produtos_exemplo):
        # Arrange: insere vários produtos
        produto_repo.criar_tabela_produtos()
        for produto in lista_produtos_exemplo:
            produto_repo.inserir_produto(produto)
        # Act: busca a segunda página com 3 produtos por página
        produtos_pagina = produto_repo.obter_produtos_por_pagina(numero_pagina=2, tamanho_pagina=3)
        # Assert: verifica se retornou a quantidade correta (2 produtos restantes)
        assert len(produtos_pagina) == 2, "Deveria retornar 2 produtos na segunda página"
        # Verifica se são os produtos corretos
        nomes_esperados = ["Produto D", "Produto E"]
        nomes_retornados = [p.nome for p in produtos_pagina]
        assert nomes_retornados == nomes_esperados, "Os produtos da segunda página não estão corretos"
    
    def test_obter_produtos_por_pagina_vazia(self, test_db):
        # Arrange: prepara o banco sem produtos
        produto_repo.criar_tabela_produtos()
        # Act: tenta buscar produtos
        produtos_pagina = produto_repo.obter_produtos_por_pagina(numero_pagina=1, tamanho_pagina=10)
        # Assert: verifica se retorna lista vazia
        assert len(produtos_pagina) == 0, "Deveria retornar lista vazia quando não há produtos"
        assert isinstance(produtos_pagina, list), "Deveria retornar uma lista"