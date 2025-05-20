CREATE_TABLE_CATEGORIA = """
CREATE TABLE IF NOT EXISTS Categoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);
"""

# Constante para inserir um novo categoria
INSERT_CATEGORIA = """
INSERT INTO Categoria (nome) 
VALUES (?);
"""

# Constante para atualizar um categoria existente
UPDATE_CATEGORIA = """
UPDATE Categoria
SET nome = ?
WHERE id = ?;
"""

# Constante para excluir um categoria pelo ID
DELETE_CATEGORIA = """
DELETE FROM Categoria
WHERE id = ?;
"""

# Constante para obter um categoria pelo ID
GET_CATEGORIA_BY_ID = """
SELECT id, nome
FROM Categoria
WHERE id = ?;
"""

# Constante para obter produtos por página (com paginação)
GET_CATEGORIAS_BY_PAGE = """
SELECT id, nome
FROM Categoria
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""