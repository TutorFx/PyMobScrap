import requests
from entities.Empreendimento import Local, LocalContact
from entities.Proxy import Proxy
from entities.Session import Session
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
        print(f"Em um total existem {len(self.locais)} locais")
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
        session = Session(proxy)

        for i in range(amount):

            try:
                if (fonte == "vivareal"):
                    response = session.get_vivareal(start + i)

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
                    
                if (fonte == "zap"):
                    response = session.get_zap(start + i)

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
            except:
                print('Erro ao obter locais')

        print(f'Foram coletados {len(locais)} locais de {fonte}')
        return self.gerenciador.add_locais(locais)

    def coletar_locais_em_threads(self, fonte, amount = 5, thread_n = 5):
        threads = []

        for i in range(thread_n):
            t = Thread(target=self.obter_locais, args=(fonte, amount, i * amount))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print(self.gerenciador.__str__())
    
    def coletar_locais_em_threads_v2(self, fonte, amount = 10, thread_n = 50):
        with ThreadPoolExecutor(max_workers=thread_n) as executor:
            for i in range(thread_n):
                executor.submit(self.obter_locais, fonte, amount, i * amount)

        print(self.gerenciador.__str__())

class ProxyCollector:
    def __init__(self):
        self.proxies = []
        self.testing_lane = []
        self.lock = Lock()

    def add_proxy(self, proxy: Proxy):
        if (isinstance(proxy, Proxy)):
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
            for proxy in Repository.get_thespeedx():
                test_proxy = Proxy(proxy.get("ip"), proxy.get("port"), proxy.get("kind"))
                self.testing_lane.append(test_proxy)
        except requests.exceptions.RequestException:
            print("Erro ao atualizar proxies de thespeedx")

        try:
            for proxy in Repository.get_free_proxy_list_net():
                test_proxy = Proxy(proxy.get("ip"), proxy.get("port"), proxy.get("kind"))
                self.testing_lane.append(test_proxy)
        except requests.exceptions.RequestException:
            print("Erro ao atualizar proxies de http://free-proxy.cz/")

        random.shuffle(self.testing_lane)

        with ThreadPoolExecutor(max_workers=200) as executor:
            executor.map(self.validate_proxies, self.testing_lane)


        #while len(self.testing_lane) > 0 and proxies
                
    def validate_proxies(self, proxy: Proxy, limit=500):
        try:
            if len(self.proxies) <= limit:
                session = requests.Session()
                response = session.get("https://api64.ipify.org", proxies={ "https": proxy.get(), "http": proxy.get() }, timeout=3)
                print(response.text)
                with self.lock:
                    self.add_proxy(proxy)
                    self.testing_lane.remove(proxy)
                print(f'Proxy {proxy.get()} validado. {len(self.proxies)}/{limit}({len(self.testing_lane)})')
        except requests.exceptions.Timeout:
            with self.lock:
                self.testing_lane.remove(proxy)
        except requests.exceptions.ConnectionError:
            with self.lock:
                self.testing_lane.remove(proxy)
            
    
    def __str__(self) -> str:
        return f'Existem no total {len(self.proxies)} proxies armazenados.'