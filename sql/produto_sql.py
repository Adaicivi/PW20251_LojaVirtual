CREATE_TABLE_PRODUTO = """
CREATE TABLE IF NOT EXISTS Produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL,
    preco REAL NOT NULL,
    estoque INTEGER NOT NULL,
    imagem TEXT NOT NULL,
    id_categoria INTEGER NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id)
);
"""

INSERT_PRODUTO = """
INSERT INTO Produto (nome, descricao, preco, estoque, imagem, id_categoria) 
VALUES (?, ?, ?, ?, ?, ?);
"""

UPDATE_PRODUTO = """
UPDATE Produto 
SET nome = ?, descricao = ?, preco = ?, estoque = ?, imagem = ?, id_categoria = ?
WHERE id = ?;
"""

DELETE_PRODUTO = """
DELETE FROM Produto 
WHERE id = ?;
"""

GET_PRODUTO_BY_ID = """
SELECT 
    p.id, 
    p.nome, 
    p.descricao, 
    p.preco, 
    p.estoque, 
    p.imagem, 
    p.id_categoria, 
    c.nome AS nome_categoria
FROM Produto p
INNER JOIN Categoria c ON p.id_categoria = c.id
WHERE p.id = ?;
"""

GET_PRODUTOS_BY_PAGE = """
SELECT 
    p.id, 
    p.nome, 
    p.descricao, 
    p.preco, 
    p.estoque, 
    p.imagem, 
    p.id_categoria, 
    c.nome AS nome_categoria
FROM Produto p
INNER JOIN Categoria c ON p.id_categoria = c.id
ORDER BY p.nome ASC
LIMIT ? OFFSET ?;
"""