from dataclasses import dataclass
import datetime


@dataclass
class Cliente:
    id: int
    nome: str
    cpf: str
    telefone: str
    email: str
    data_nascimento: datetime
