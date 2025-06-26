from dataclasses import dataclass
from typing import Optional


@dataclass
class Endereco:
    id: int
    logradouro: str
    numero: str
    complemento: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    id_usuario: int