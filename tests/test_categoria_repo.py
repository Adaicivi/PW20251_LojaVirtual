import os
import sys
from repo.categoria_repo import *
from models.categoria import Categoria

class TestCategoriaRepo:
    def test_criar_tabela_categorias(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_categorias()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_categoria(self, test_db):
        # Arrange
        criar_tabela_categorias()
        categoria_teste = Categoria(0, "Categoria Teste")
        # Act
        id_categoria_inserida = inserir_categoria(categoria_teste)
        # Assert
        categoria_db = obter_categoria_por_id(id_categoria_inserida)
        assert categoria_db is not None, "A categoria inserida não deveria ser None"
        assert categoria_db.id == 1, "A categoria inserida deveria ter um ID igual a 1"
        assert categoria_db.nome == "Categoria Teste", "O nome da categoria inserida não confere"

    def test_atualizar_categoria(self, test_db):
        # Arrange
        criar_tabela_categorias()
        categoria_teste = Categoria(0, "Categoria Teste")
        id_categoria_inserida = inserir_categoria(categoria_teste)
        categoria_inserida = obter_categoria_por_id(id_categoria_inserida)
        # Act
        categoria_inserida.nome = "Categoria Atualizada"
        resultado = atualizar_categoria(categoria_inserida)
        # Assert
        assert resultado == True, "A atualização da categoria deveria retornar True"
        categoria_db = obter_categoria_por_id(id_categoria_inserida)
        assert categoria_db.nome == "Categoria Atualizada", "O nome da categoria atualizada não confere"

    def test_excluir_categoria(self, test_db):
        # Arrange
        criar_tabela_categorias()
        categoria_teste = Categoria(0, "Categoria Teste")
        id_categoria_inserida = inserir_categoria(categoria_teste)
        # Act
        resultado = excluir_categoria(id_categoria_inserida)
        # Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        categoria_excluida = obter_categoria_por_id(id_categoria_inserida)
        assert categoria_excluida == None, "A categoria excluída deveria ser None"

    def test_obter_categoria_por_id(self, test_db):
        # Arrange
        criar_tabela_categorias()
        categoria_teste = Categoria(0, "Categoria Teste")
        id_categoria_inserida = inserir_categoria(categoria_teste)
        # Act
        categoria_db = obter_categoria_por_id(id_categoria_inserida)
        # Assert
        assert categoria_db is not None, "A categoria retornada deveria ser diferente de None"
        assert categoria_db.id == id_categoria_inserida, "O id da categoria buscada deveria ser igual ao id da categoria inserida"
        assert categoria_db.nome == categoria_teste.nome, "O nome da categoria buscada deveria ser igual ao nome da categoria inserida"

    def test_obter_categorias_por_pagina(self, test_db):
        # Arrange
        criar_tabela_categorias()
        for i in range(10):
            categoria = Categoria(0, f"Categoria {i+1}")
            inserir_categoria(categoria)
        # Act
        categorias_1 = obter_categorias_por_pagina(1, 10)
        categorias_2 = obter_categorias_por_pagina(2, 4)
        categorias_3 = obter_categorias_por_pagina(3, 4)
        # Assert
        assert len(categorias_1) == 10, "A primeira consulta deveria ter retornado 10 categorias"
        assert len(categorias_2) == 4, "A segunda consulta deveria ter retornado 4 categorias"
        assert len(categorias_3) == 2, "A terceira consulta deveria ter retornado 2 categorias"
        assert categorias_3[0].id == 8, "A primeira categoria da terceira página de tamanho 4 deveria ter id igual a 8"

