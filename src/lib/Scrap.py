import requests
from entities.Empreendimento import Local, LocalContact
from entities.Proxy import Proxy
import utils.Repository as Repository
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor
import random

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
        self.proxy_collector = ProxyCollector()

    def coletar_e_adicionar_locais(self, fonte):
        self.obter_locais(fonte)
        print(self.gerenciador.__str__())

    def obter_locais(self, fonte, amount = 1, start = 0):
        # Aqui você pode adicionar a lógica para obter os objetos Local de uma fonte
        # Por enquanto, vamos retornar uma lista vazia
        locais = []
        proxy = self.proxy_collector.get_random_proxy()

        for i in range(amount):

            try:
                if (fonte == "vivareal"):
                    response = Repository.get_vivareal_data(proxy, start + i)

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
                    
                if (fonte == "imoveis"):
                    #blabla
                    return;

            except requests.exceptions.RequestException as e:
                print(f'Ocorreu um erro ao se conectar com {fonte}', e)
            except:
                print('Erro ao obter locais')
                raise;

        print(f'Foram coletados {len(locais)} locais de {fonte}')
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

class ProxyCollector:
    def __init__(self):
        self.proxies = []
        self.testing_lane = []
        self.lock = Lock()

    def add_proxy(self, proxy: Proxy):
        with self.lock:
            if (isinstance(proxy, Proxy)):
                print(proxy.__str__())
                self.proxies.append(proxy)

    def get_proxies(self):
        return self.proxies
    
    def get_random_proxy(self):
        if len(self.proxies) == 0:
            print("Não existem proxies armazenados")
            raise Exception("Não existem proxies válidos")

        return random.choice(self.proxies)
    
    def scrap_proxies(self):

        try:
            for proxy in Repository.get_free_proxy_cz():
                test_proxy = Proxy(proxy.get("ip"), proxy.get("port"), proxy.get("kind"))
                self.testing_lane.append(test_proxy)
        except requests.exceptions.RequestException:
            print("Erro ao atualizar proxies de http://free-proxy-list.net/")
        
        try:
            for proxy in Repository.get_free_proxy_list_net():
                test_proxy = Proxy(proxy.get("ip"), proxy.get("port"), proxy.get("kind"))
                self.testing_lane.append(test_proxy)
        except requests.exceptions.RequestException:
            print("Erro ao atualizar proxies de http://free-proxy.cz/")

        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.validate_proxies, self.testing_lane)

        #while len(self.testing_lane) > 0 and proxies
                
    def validate_proxies(self, proxy: Proxy):

        try:
            requests.get("https://api64.ipify.org", proxies={ "https": proxy.get(), "http": proxy.get() }, timeout=3)
            with self.lock:
                print(f"Proxy adicionado. {proxy.get()}")
                self.add_proxy(proxy)
        except requests.exceptions.Timeout:
            with self.lock:
                print(f"Proxy lento removido. {proxy.get()}")
                self.testing_lane.remove(proxy)
        except requests.exceptions.ConnectionError:
            with self.lock:
                print(f"Proxy não funcional removido. {proxy.get()}")
                self.testing_lane.remove(proxy)
    
    def __str__(self) -> str:
        return f'Existem no total {len(self.proxies)} proxies armazenados.'