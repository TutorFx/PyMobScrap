import time
from typing import Union

class LocalContact:
    """Local Owner Class"""
    def __init__(self, nome: str, telefone: Union[str, None], celular: Union[str, None], cresci: str, tier: Union[str, None] = None, ):
        self.nome = nome
        self.telefone = telefone
        self.celular = celular
        self.cresci = cresci
        self.tier = tier

    def __str__(self):
        return f'Nome: {self.nome} e telefone {self.telefone} e celular {self.celular}'

class Local:
    """Local Class"""
    def __init__(self, nome: str, preco: str, url: str, owner: LocalContact, time: float = time.time(), ):
        self.nome = nome
        self.preco = preco
        self.url = url
        self.owner = owner
        self.time = time
