CREATE_TABLE_ENDERECO = """
CREATE TABLE IF NOT EXISTS Endereco (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    logradouro TEXT NOT NULL,
    numero TEXT NOT NULL,
    complemento TEXT,
    bairro TEXT NOT NULL,
    cidade TEXT NOT NULL,
    uf TEXT NOT NULL,
    cep TEXT NOT NULL
);
""" 

# Constante para inserir um novo endereco
INSERT_ENDERECO = """
INSERT INTO Endereco (logradouro, numero, complemento, bairro, cidade, uf, cep) 
VALUES (?);
"""

# Constante para atualizar um endereco existente
UPDATE_ENDERECO = """
UPDATE Endereco
SET logradouro = ?, numero = ?, complemento = ?, bairro = ?, cidade = ?, uf = ?, cep = ?
WHERE id = ?;
"""

# Constante para excluir um endereco pelo ID
DELETE_ENDERECO = """
DELETE FROM Endereco
WHERE id = ?;
"""

# Constante para obter um endereco pelo ID
GET_ENDERECO_BY_ID = """
SELECT id, logradouro, numero, complemento, bairro, cidade, uf, cep
FROM Endereco
WHERE id = ?;
"""

# Constante para obter produtos por página (com paginação)
GET_ENDERECOS_BY_PAGE = """
SELECT id, logradouro, numero, complemento, bairro, cidade, uf, cep
FROM Endereco
ORDER BY logradouro ASC
LIMIT ? OFFSET ?;
"""