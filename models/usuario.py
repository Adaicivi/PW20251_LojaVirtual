from dataclasses import dataclass
import datetime
from typing import Optional


@dataclass
class Usuario:
    id: int
    nome: str
    cpf: str
    telefone: str
    email: str    
    data_nascimento: datetime
    senha_hash: Optional[str] = None
    tipo: int = 0

    