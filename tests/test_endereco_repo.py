from repo import endereco_repo, usuario_repo

class TestEnderecoRepo:
    def test_criar_tabela_enderecos(self, test_db):
        # Arrange: prepara o banco de dados para criar a tabela
        # Act: chama o método para criar a tabela
        resultado = endereco_repo.criar_tabela_enderecos()
        # Assert: verifica se a tabela foi criada com sucesso
        assert resultado == True, "A tabela de endereços deveria ser criada com sucesso"
    
    def test_inserir_endereco(self, test_db, endereco_exemplo, usuario_exemplo):
        # Arrange: prepara o banco e cria a tabela
        usuario_repo.criar_tabela_usuarios()
        usuario_repo.inserir_usuario(usuario_exemplo)
        endereco_repo.criar_tabela_enderecos()
        # Act: insere o endereço de exemplo
        id_endereco_inserido = endereco_repo.inserir_endereco(endereco_exemplo)
        # Assert: verifica se o endereço foi inserido corretamente
        endereco_inserido = endereco_repo.obter_endereco_por_id(id_endereco_inserido)
        assert endereco_inserido is not None, "O endereço inserido não deveria ser None"
        assert endereco_inserido.id > 0, "O endereço inserido deveria ter um ID válido"
        assert endereco_inserido.logradouro == endereco_exemplo.logradouro, "A rua do endereço não confere"
        assert endereco_inserido.numero == endereco_exemplo.numero, "O número do endereço não confere"
        assert endereco_inserido.complemento == endereco_exemplo.complemento, "O complemento do endereço não confere"
        assert endereco_inserido.bairro == endereco_exemplo.bairro, "O bairro do endereço não confere"
        assert endereco_inserido.cidade == endereco_exemplo.cidade, "A cidade do endereço não confere"
        assert endereco_inserido.estado == endereco_exemplo.estado, "O estado do endereço não confere"
        assert endereco_inserido.cep == endereco_exemplo.cep, "O CEP do endereço não confere"
        assert endereco_inserido.id_usuario == endereco_exemplo.id_usuario, "O ID do usuário do endereço não confere"

    def test_atualizar_endereco_existente(self, test_db, endereco_exemplo, usuario_exemplo):
        # Arrange: prepara o banco e cria a tabela
        usuario_repo.criar_tabela_usuarios()
        usuario_repo.inserir_usuario(usuario_exemplo)
        endereco_repo.criar_tabela_enderecos()
        id_endereco_inserido = endereco_repo.inserir_endereco(endereco_exemplo)
        endereco_inserido = endereco_repo.obter_endereco_por_id(id_endereco_inserido)
        # Act: atualiza o endereço inserido
        endereco_inserido.logradouro = "Rua Atualizada"
        resultado = endereco_repo.atualizar_endereco(endereco_inserido)
        # Assert: verifica se a atualização foi bem-sucedida
        assert resultado == True, "A atualização do endereço deveria retornar True"
        endereco_atualizado = endereco_repo.obter_endereco_por_id(id_endereco_inserido)
        assert endereco_atualizado.logradouro == "Rua Atualizada", "O logradouro atualizado não confere"

    def test_atualizar_endereco_inexistente(self, test_db, endereco_exemplo):
        # Arrange: prepara o banco e cria a tabela
        endereco_repo.criar_tabela_enderecos()
        endereco_exemplo.id = 999  # ID que não existe
        # Act: tenta atualizar o endereço inexistente
        resultado = endereco_repo.atualizar_endereco(endereco_exemplo)
        # Assert: verifica se a atualização falhou
        assert resultado == False, "A atualização de um endereço inexistente deveria retornar False"

    def test_excluir_endereco_existente(self, test_db, endereco_exemplo, usuario_exemplo):
        # Arrange: prepara o banco e cria a tabela
        usuario_repo.criar_tabela_usuarios()
        usuario_repo.inserir_usuario(usuario_exemplo)
        endereco_repo.criar_tabela_enderecos()
        id_endereco_inserido = endereco_repo.inserir_endereco(endereco_exemplo)
        # Act: exclui o endereço inserido
        resultado = endereco_repo.excluir_endereco(id_endereco_inserido)
        # Assert: verifica se a exclusão foi bem-sucedida
        assert resultado == True, "A exclusão do endereço deveria retornar True"
        endereco_excluido = endereco_repo.obter_endereco_por_id(id_endereco_inserido)
        assert endereco_excluido is None, "O endereço excluído deveria ser None"

    def test_excluir_endereco_inexistente(self, test_db):
        # Arrange: prepara o banco e cria a tabela
        usuario_repo.criar_tabela_usuarios()
        endereco_repo.criar_tabela_enderecos()
        # Act: tenta excluir um endereço inexistente
        resultado = endereco_repo.excluir_endereco(999)
        # Assert: verifica se a exclusão falhou
        assert resultado == False, "A exclusão de um endereço inexistente deveria retornar False"

    def test_obter_endereco_por_id_existente(self, test_db, endereco_exemplo, usuario_exemplo):
        # Arrange: prepara o banco e cria a tabela
        usuario_repo.criar_tabela_usuarios()
        usuario_repo.inserir_usuario(usuario_exemplo)
        endereco_repo.criar_tabela_enderecos()
        id_endereco_inserido = endereco_repo.inserir_endereco(endereco_exemplo)
        # Act: obtém o endereço pelo ID
        endereco_obtido = endereco_repo.obter_endereco_por_id(id_endereco_inserido)
        # Assert: verifica se o endereço foi obtido corretamente
        assert endereco_obtido is not None, "O endereço obtido não deveria ser None"
        assert endereco_obtido.id == id_endereco_inserido, "O ID do endereço obtido não confere"
        assert endereco_obtido.logradouro == endereco_exemplo.logradouro, "O logradouro do endereço obtido não confere"

    def test_obter_endereco_por_id_inexistente(self, test_db):
        # Arrange: prepara o banco e cria a tabela
        endereco_repo.criar_tabela_enderecos()
        # Act: tenta obter um endereço inexistente
        endereco_obtido = endereco_repo.obter_endereco_por_id(999)
        # Assert: verifica se o resultado é None
        assert endereco_obtido is None, "O endereço obtido com ID inexistente deveria ser None"

    def test_obter_enderecos_por_usuario(self, test_db, endereco_exemplo, usuario_exemplo):
        # Arrange: prepara o banco e cria a tabela
        usuario_repo.criar_tabela_usuarios()
        id_usuario_inserido = usuario_repo.inserir_usuario(usuario_exemplo)
        endereco_repo.criar_tabela_enderecos()
        # Insere 3 endereços para o usuário
        for i in range(3):
            endereco_exemplo.id_usuario = id_usuario_inserido
            endereco_exemplo.logradouro = f"Rua {i+1}"
            endereco_repo.inserir_endereco(endereco_exemplo)
        # Act: obtém os endereços do usuário
        enderecos_obtidos = endereco_repo.obter_enderecos_por_usuario(id_usuario_inserido)
        # Assert: verifica se os endereços foram obtidos corretamente
        assert len(enderecos_obtidos) == 3, "Deveria retornar 3 endereços para o usuário"
        assert all(isinstance(e, endereco_repo.Endereco) for e in enderecos_obtidos), "Todos os itens retornados devem ser do tipo Endereco"

    def test_obter_enderecos_por_usuario_vazio(self, test_db, usuario_exemplo):
        # Arrange: prepara o banco e cria a tabela
        usuario_repo.criar_tabela_usuarios()
        id_usuario_inserido = usuario_repo.inserir_usuario(usuario_exemplo)
        endereco_repo.criar_tabela_enderecos()
        # Act: obtém os endereços de um usuário sem endereços
        enderecos_obtidos = endereco_repo.obter_enderecos_por_usuario(id_usuario_inserido)
        # Assert: verifica se o resultado é uma lista vazia
        assert isinstance(enderecos_obtidos, list), "Deveria retornar uma lista"
        assert len(enderecos_obtidos) == 0, "Deveria retornar uma lista vazia para usuário sem endereços"

    def test_obter_enderecos_por_usuario_inexistente(self, test_db):
        # Arrange: prepara o banco e cria a tabela
        endereco_repo.criar_tabela_enderecos()
        # Act: tenta obter endereços de um usuário inexistente
        enderecos_obtidos = endereco_repo.obter_enderecos_por_usuario(999)
        # Assert: verifica se o resultado é uma lista vazia
        assert len(enderecos_obtidos) == 0, "Deveria retornar uma lista vazia para usuário inexistente"
