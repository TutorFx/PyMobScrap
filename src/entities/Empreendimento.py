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
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "telefone": self.telefone,
            "celular": self.celular,
            "cresci": self.cresci,
            "tier": self.tier,
        }

class Local:
    """Local Class"""
    def __init__(self, nome: str, preco: str, url: str, owner: LocalContact, time: float = time.time(), ):
        self.nome = nome
        self.preco = preco
        self.url = url
        self.owner = owner
        self.time = time

    def to_dict(self):
        return {
            "nome": self.nome,
            "preco": self.preco,
            "url": self.url,
            "owner": self.owner.to_dict(),
            "time": self.time,
        }
    
    @staticmethod
    def from_dict(dict_obj):
        owner = LocalContact(**dict_obj['owner'])
        return Local(owner=owner, **{k: v for k, v in dict_obj.items() if k != 'owner'})

def mock_local():
    contact = LocalContact(nome="Teste", telefone="(11) 1111-1111", celular="(11) 1111-1111", cresci="Teste")
    return Local(nome="Teste", preco="Teste", url="Teste", owner=contact)