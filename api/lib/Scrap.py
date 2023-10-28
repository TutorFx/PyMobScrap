import requests
from entities.Empreendimento import Local, LocalContact
import utils.Repository as Repository
from threading import Thread, Lock

class GerenciadorDeLocais:
    def __init__(self):
        self.locais = []  # Este é o atributo que irá armazenar as instâncias de Local
        self.lock = Lock()

    def add_local(self, local):
        with self.lock:
            if isinstance(local, Local):
                self.locais.append(local)
            else:
                print("Erro: o argumento deve ser uma instância da classe Local")

    def add_locais(self, locais: list):
        for local in locais:
            self.add_local(local)

    def get_locais(self):
        return self.locais
    
    def __str__(self) -> str:
        return f'Existem no total {len(self.locais)} locais armazenados no Gerenciador.'


class ColetorDeLocais:
    def __init__(self):
        self.gerenciador = GerenciadorDeLocais()

    def coletar_e_adicionar_locais(self, fonte):
        self.obter_locais(fonte)
        print(self.gerenciador.__str__())

    def obter_locais(self, fonte, amount = 5, start = 0):
        # Aqui você pode adicionar a lógica para obter os objetos Local de uma fonte
        # Por enquanto, vamos retornar uma lista vazia
        locais = []
        for i in range(amount):

            try:
                if (fonte == "vivareal"):
                    response = Repository.get_vivareal_data(start + i)
                    
                    for item in response["body"]:
                        account = item["account"]
                        owner = LocalContact(
                            account.get("name"),
                            account.get("phones", {}).get("primary"),
                            account.get("phones", {}).get("mobile"),
                            account.get("licenseNumber"),
                            account.get("tier"),
                        )
                        local = Local(
                            item.get("link", {}).get("name"),
                            item.get("listing", {}).get(
                                "pricingInfos", [{}])[0].get("price"),
                            item.get("link", {}).get("href"),
                            owner
                        )
                        locais.append(local)
            except requests.exceptions.RequestException as e:
                print(f'Ocorreu um erro ao se conectar com {fonte}', e)
                print(f'{e.__cause__}')
            except:
                print('Erro ao obter locais')
                raise
        return self.gerenciador.add_locais(locais)

    def coletar_locais_em_threads(self, fonte, amount = 5, thread_n = 1):
        threads = []

        for i in range(thread_n):
            t = Thread(target=self.obter_locais, args=(fonte, amount, i * amount))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print(self.gerenciador.__str__())