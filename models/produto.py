from dataclasses import dataclass
from typing import Optional

from models.categoria import Categoria

@dataclass
class Produto:
    id: int
    nome: str
    descricao: str
    preco: float
    estoque: int
    imagem: str
    id_categoria: int
    categoria: Optional[Categoria] = None