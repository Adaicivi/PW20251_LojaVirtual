from util.database import obter_conexao
from repo import usuario_repo, endereco_repo, categoria_repo, produto_repo

def criar_tabelas():
    usuario_repo.criar_tabela_usuarios()
    endereco_repo.criar_tabela_enderecos()
    categoria_repo.criar_tabela_categorias()
    produto_repo.criar_tabela_produtos()

def inserir_dados_iniciais():
    # Obtém a conexão com o banco de dados
    conexao = obter_conexao()
    # Insere dados iniciais nas tabelas usando a mesma conexão para evitar problemas de concorrência
    usuario_repo.inserir_dados_iniciais(conexao)
    endereco_repo.inserir_dados_iniciais(conexao)
    categoria_repo.inserir_dados_iniciais(conexao)
    produto_repo.inserir_dados_iniciais(conexao)
    # Commit para garantir que as alterações sejam salvas
    conexao.commit()
    # Fecha a conexão após inserir os dados
    conexao.close()