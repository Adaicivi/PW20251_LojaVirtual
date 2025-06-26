from repo import categoria_repo

class TestCategoriaRepo:
    def test_criar_tabela_categorias(self, test_db):
        # Arrange
        # Act
        resultado = categoria_repo.criar_tabela_categorias()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_categoria(self, test_db, categoria_exemplo):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        # Act
        id_categoria_inserida = categoria_repo.inserir_categoria(categoria_exemplo)
        # Assert
        categoria_db = categoria_repo.obter_categoria_por_id(id_categoria_inserida)
        assert categoria_db is not None, "A categoria inserida não deveria ser None"
        assert categoria_db.id == 1, "A categoria inserida deveria ter um ID igual a 1"
        assert categoria_db.nome == "Categoria Teste", "O nome da categoria inserida não confere"

    def test_obter_categoria_por_id_existente(self, test_db, categoria_exemplo):
        # Arrange
        categoria_repo.criar_tabela_categorias()        
        id_categoria_inserida = categoria_repo.inserir_categoria(categoria_exemplo)
        # Act
        categoria_db = categoria_repo.obter_categoria_por_id(id_categoria_inserida)
        # Assert
        assert categoria_db is not None, "A categoria retornada deveria ser diferente de None"
        assert categoria_db.id == id_categoria_inserida, "O id da categoria buscada deveria ser igual ao id da categoria inserida"
        assert categoria_db.nome == categoria_exemplo.nome, "O nome da categoria buscada deveria ser igual ao nome da categoria inserida"

    def test_obter_categoria_por_id_inexistente(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        # Act
        categoria_db = categoria_repo.obter_categoria_por_id(999)
        # Assert
        assert categoria_db is None, "A categoria buscada com ID inexistente deveria retornar None"

    def test_atualizar_categoria_existente(self, test_db, categoria_exemplo):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        id_categoria_inserida = categoria_repo.inserir_categoria(categoria_exemplo)
        categoria_inserida = categoria_repo.obter_categoria_por_id(id_categoria_inserida)
        # Act
        categoria_inserida.nome = "Categoria Atualizada"
        resultado = categoria_repo.atualizar_categoria(categoria_inserida)
        # Assert
        assert resultado == True, "A atualização da categoria deveria retornar True"
        categoria_db = categoria_repo.obter_categoria_por_id(id_categoria_inserida)
        assert categoria_db.nome == "Categoria Atualizada", "O nome da categoria atualizada não confere"

    def test_atualizar_categoria_inexistente(self, test_db, categoria_exemplo):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        categoria_exemplo.id = 999  # ID que não existe
        # Act
        resultado = categoria_repo.atualizar_categoria(categoria_exemplo)
        # Assert
        assert resultado == False, "A atualização de uma categoria inexistente deveria retornar False"

    def test_excluir_categoria_existente(self, test_db, categoria_exemplo):
        # Arrange
        categoria_repo.criar_tabela_categorias()        
        id_categoria_inserida = categoria_repo.inserir_categoria(categoria_exemplo)
        # Act
        resultado = categoria_repo.excluir_categoria(id_categoria_inserida)
        # Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        categoria_excluida = categoria_repo.obter_categoria_por_id(id_categoria_inserida)
        assert categoria_excluida is None, "A categoria excluída deveria ser None"

    def test_excluir_categoria_inexistente(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        # Act
        resultado = categoria_repo.excluir_categoria(999)
        # Assert
        assert resultado == False, "A exclusão de uma categoria inexistente deveria retornar False"

    def test_obter_categorias_por_pagina_primeira_pagina(self, test_db, lista_categorias_exemplo):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        for categoria in lista_categorias_exemplo:
            categoria_repo.inserir_categoria(categoria)
        # Act
        pagina_categorias = categoria_repo.obter_categorias_por_pagina(1, 4)        
        # Assert
        assert len(pagina_categorias) == 4, "A primeira consulta deveria ter retornado 4 categorias"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [categoria.id for categoria in pagina_categorias]
        assert ids_retornados == ids_esperados, "Os IDs das categorias retornadas não estão corretos"

    def test_obter_categorias_por_pagina_terceira_pagina(self, test_db, lista_categorias_exemplo):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        for categoria in lista_categorias_exemplo:
            categoria_repo.inserir_categoria(categoria)
        # Act
        pagina_categorias = categoria_repo.obter_categorias_por_pagina(3, 4)
        # Assert
        assert len(pagina_categorias) == 2, "A terceira pagina deveria ter retornado 2 categorias"
        ids_esperados = [9, 10]
        ids_retornados = [categoria.id for categoria in pagina_categorias]
        assert ids_retornados == ids_esperados, "Os IDs das categorias retornadas na terceira página não estão corretos"

    def test_obter_categorias_por_pagina_vazia(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        # Act
        pagina_categorias = categoria_repo.obter_categorias_por_pagina(1, 10)
        # Assert
        assert isinstance(pagina_categorias, list), "Deveria retornar uma lista"
        assert len(pagina_categorias) == 0, "Deveria retornar lista vazia quando não há categorias"