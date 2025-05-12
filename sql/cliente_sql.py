CREATE_TABLE_CLIENTE = """
CREATE TABLE IF NOT EXISTS cliente (
    i INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    data_nascimento TEXT NOT NULL);
"""

INSERT_CLIENTE = """
INSERT INTO cliente (nome, cpf, telefone, email, data_nascimento)
VALUES (?, ?, ?, ?, ?);
"""

UPDATE_CLIENTE = """
UPDATE cliente
SET nome = ?, cpf = ?, telefone = ?, email = ?, data_nascimento = ?
WHERE id = ?;
"""
DELETE_CLIENTE = """
DELETE FROM cliente
WHERE id = ?;
"""
GET_CLIENTE_BY_ID = """
SELECT id, nome, cpf, telefone, email, data_nascimento 
FROM cliente
WHERE id = ?;
"""
GET_CLIENTES_BY_PAGE = """
SELECT id, nome, cpf, telefone, email, data_nascimento
FROM cliente
ORDER BY nome_ASC
LIMIT ? OFFSET ?;
"""
