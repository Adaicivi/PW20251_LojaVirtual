CREATE_TABLE_ENDERECO = """
CREATE TABLE IF NOT EXISTS Endereco (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    logradouro VARCHAR(255) NOT NULL,
    numero VARCHAR(10) NOT NULL,
    complemento VARCHAR(255),
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL,
    cep VARCHAR(10) NOT NULL,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id) ON DELETE CASCADE
);
"""

INSERT_ENDERECO = """
INSERT INTO Endereco (logradouro, numero, complemento, bairro, cidade, estado, cep, id_usuario)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

UPDATE_ENDERECO = """
UPDATE Endereco
SET logradouro = ?, numero = ?, complemento = ?, bairro = ?, cidade = ?, estado = ?, cep = ?
WHERE id = ?
"""

DELETE_ENDERECO = """
DELETE FROM Endereco
WHERE id = ?
"""

GET_ENDERECO_BY_ID = """
SELECT id, logradouro, numero, complemento, bairro, cidade, estado, cep, id_usuario
FROM Endereco
WHERE id = ?
"""

GET_ENDERECOS_BY_ID_USUARIO = """
SELECT id, logradouro, numero, complemento, bairro, cidade, estado, cep, id_usuario
FROM Endereco
WHERE id_usuario = ?
"""