from models.usuario import Usuario
from repo.usuario_repo import *

class TestUsuarioRepo:

    def test_atualizar_senha_usuario(self, test_db):
        # Arrange
        criar_tabela_usuarios()
        usuario_teste = Usuario(0, "Usuario Teste", "123456789-00", "(28) 99999-8888", "fulano@email.com", "2000-01-15", "123456", 0)
        id_usuario_inserido = inserir_usuario(usuario_teste)
        # Act
        resultado = atualizar_senha_usuario(id_usuario_inserido, "654321")
        # Assert
        assert resultado == True, "A atualização de senha deveria retornar True"
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        usuario_alterado = obter_usuario_por_email(usuario_db.email)
        assert usuario_alterado is not None, "O usuário inserido não pode ser None"
        assert usuario_alterado.senha_hash == "654321"