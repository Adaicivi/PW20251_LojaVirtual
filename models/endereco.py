from dataclasses import dataclass


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
