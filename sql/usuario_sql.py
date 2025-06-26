CREATE_TABLE_USUARIO = """
CREATE TABLE IF NOT EXISTS Usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    data_nascimento TEXT NOT NULL,
    senha_hash TEXT NOT NULL,
    tipo INTEGER NOT NULL DEFAULT 0);
"""

INSERT_USUARIO = """
INSERT INTO Usuario (nome, cpf, telefone, email, data_nascimento, senha_hash)
VALUES (?, ?, ?, ?, ?, ?);
"""

UPDATE_USUARIO = """
UPDATE Usuario
SET nome = ?, cpf = ?, telefone = ?, email = ?, data_nascimento = ?
WHERE id = ?;
"""

UPDATE_TIPO_USUARIO = """
UPDATE Usuario
SET tipo = ?
WHERE id = ?;
"""

UPDATE_SENHA_USUARIO = """
UPDATE Usuario
SET senha_hash = ?
WHERE id = ?;
"""

DELETE_USUARIO = """
DELETE FROM Usuario
WHERE id = ?;
"""

GET_USUARIO_BY_ID = """
SELECT id, nome, cpf, telefone, email, data_nascimento, senha_hash, tipo
FROM Usuario
WHERE id = ?;
"""

GET_USUARIO_BY_EMAIL = """
SELECT id, nome, cpf, telefone, email, data_nascimento, senha_hash, tipo
FROM Usuario
WHERE email = ?;
"""

GET_USUARIOS_BY_PAGE = """
SELECT id, nome, cpf, telefone, email, data_nascimento, tipo
FROM Usuario
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""