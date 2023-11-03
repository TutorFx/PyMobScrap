import time as t
from typing import Union


class LocalContact:
    """
    Initialize a LocalContact object.

    Args:
    - nome (str): The name of the local owner.
    - telefone (Union[str, None]): The telephone number of the local owner.
    - celular (Union[str, None]): The cellphone number of the local owner.
    - cresci (str): The cresci of the local owner.
    - tier (Union[str, None], optional): The tier of the local owner. Defaults to None.
    """

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


    def __init__(self, nome: str, preco: str, url: str, owner: LocalContact, cep: str, origin: str, business: str, lat: Union[str, None] = None, lon: Union[str, None] = None, time: float = t.time(), ):
        """
        Initialize a Local object.

        Args:
        - nome (str): The name of the local.
        - preco (str): The price of the local.
        - url (str): The URL of the local.
        - owner (LocalContact): The owner of the local.
        - cep (str): The CEP of the local.
        - origin (str): The origin of the local.
        - business (str): The business of the local.
        - lat (Union[str, None], optional): The latitude of the local. Defaults to None.
        - lon (Union[str, None], optional): The longitude of the local. Defaults to None.
        - time (float, optional): The time of creation of the local. Defaults to the current time.
        """
        self.nome = nome
        self.preco = preco
        self.url = url
        self.owner = owner
        self.cep = cep
        self.lat = lat
        self.lon = lon
        self.business = business
        self.origin = origin
        self.time = time

    def to_dict(self):
        """
        Convert the Local object to a dictionary.

        Returns:
        - dict: The Local object as a dictionary.
        """
        return {
            "nome": self.nome,
            "preco": self.preco,
            "url": self.url,
            "owner": self.owner.to_dict(),
            "cep": self.cep,
            "lat": self.lat,
            "lon": self.lon,
            "business": self.business,
            "origin": self.origin,
            "time": self.time,
        }

    @staticmethod
    def from_dict(dict_obj):
        """
        Create a Local object from a dictionary.

        Args:
        - dict_obj (dict): The dictionary representing the Local object.

        Returns:
        - Local: The Local object created from the dictionary.
        """
        owner = LocalContact(**dict_obj['owner'])
        owner_dict = dict_obj.get('owner')
        if owner_dict is None:
            raise ValueError("Missing 'owner' key in dictionary")
        return Local(owner=owner, **{k: v for k, v in dict_obj.items() if k != 'owner'})


def mock_local():
    """
    Create a mock Local object for testing.

    Returns:
    - Local: The mock Local object.
    """
    contact = LocalContact(nome="Teste", telefone="(11) 1111-1111",
                           celular="(11) 1111-1111", cresci="Teste")
    return Local(
        nome="Teste",
        preco="Teste",
        url="Teste",
        cep="Teste",
        origin="Teste",
        business="Teste",
        lat=None,
        lon=None,
        owner=contact
    )
