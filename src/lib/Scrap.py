import os
from typing import Union
import requests
import cloudscraper
from entities.Empreendimento import Local, LocalContact, mock_local
from entities.Proxy import Proxy
from entities.Session import Session
import utils.Repository as Repository
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor
import json
import random

class GerenciadorDeLocais:
    def __init__(self):
        self.locais = []  # Este é o atributo que irá armazenar as instâncias de Local
        self.lock = Lock()
        self.storage = "./src/cache/locais.json"

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
    
    def carregar_locais(self):
        if not os.path.isfile(self.storage):
            # Se não existir, cria o arquivo
            with open(self.storage, 'w') as file: 
                json.dump([], file)
        with open(self.storage, 'r') as file:
            locais_dict = json.load(file)
            self.locais = [Local.from_dict(local_dict) for local_dict in locais_dict]
    
    def salvar_locais(self):
        with open(self.storage, 'w') as file:
            locais_dict = [local.to_dict() for local in self.locais]
            json.dump(locais_dict, file)
    
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
        session = self.proxy_collector.get_random_session()
        if not isinstance(session, Session):
            print("Erro: não foi possível obter uma sessão válida")
            return;
    
        for i in range(amount):
            start_from = start + i

            
            def request_vivareal(start_from):
                response = session.get_vivareal(start_from)

                for local in Repository.glue_api_formatter(response):
                    locais.append(local)

                return True

            def request_zap(start_from):
                response = session.get_zap(start_from)

                for local in Repository.glue_api_formatter(response):
                    locais.append(local)

                return True
            
            for _ in range(15):
                try: 
                    if (fonte == "vivareal"):
                        request_vivareal(start_from)

                    if (fonte == "zap"):
                        request_zap(start_from)
                    break;
                
                except requests.exceptions.ProxyError as e:
                    print(f'Erro: Proxy {session.proxy.get()} não está disponível {fonte} ({_})', e.errno)
                    # Obtenha uma nova sessão e tente novamente
                    session = self.proxy_collector.get_random_session()
                except requests.exceptions.Timeout as e:
                    print(f'Erro: {fonte} demorou muito para responder ({_})', e.errno)
                    # Obtenha uma nova sessão e tente novamente
                    session = self.proxy_collector.get_random_session()
                except requests.exceptions.ConnectionError:
                    print(f'Erro: Ocorreu um erro ao se conectar com {fonte} ({_})', e.errno)
                    # Obtenha uma nova sessão e tente novamente
                    session = self.proxy_collector.get_random_session()
                except requests.exceptions.RequestException as e:
                    print(f'Ocorreu um erro ao se conectar com {fonte} ({_})', e.errno)
                    # Obtenha uma nova sessão e tente novamente
                    session = self.proxy_collector.get_random_session()
                except Exception as e:
                    print(f'Erro ao obter locais ({_})', e.errno)



        print(f'Foram coletados {len(locais)} locais de {fonte}')
        return self.gerenciador.add_locais(locais)
    
    def coletar_locais_em_threads_v2(self, fonte, amount = 10, thread_n = 25):
        with ThreadPoolExecutor(max_workers=thread_n) as executor:
            for i in range(thread_n):
                executor.submit(self.obter_locais, fonte, amount, i * amount)

        print(self.gerenciador.__str__())

class ProxyCollector:
    def __init__(self):
        self.sessions = []
        self.testing_lane = []
        self.lock = Lock()

    def add_session(self, session: Session):
        if (isinstance(session, Session)):
            self.sessions.append(session)

    def get_proxies(self):
        return self.sessions
    
    def get_random_session(self):
        if len(self.sessions) == 0:
            print("Não existem proxies armazenados")
            raise Exception("Não existem proxies válidos")

        return random.choice(self.sessions)
    
    def scrap_proxies(self):

        try:
            for proxy in Repository.get_proxy_blue():
                test_proxy = Proxy(proxy.get("ip"), proxy.get("port"), proxy.get("kind"))
                self.testing_lane.append(test_proxy)
        except requests.exceptions.ConnectionError:
            print("Erro ao atualizar proxies de http://free-proxy-list.net/")
        
        try:
            for proxy in Repository.get_thespeedx():
                test_proxy = Proxy(proxy.get("ip"), proxy.get("port"), proxy.get("kind"))
                self.testing_lane.append(test_proxy)
        except requests.exceptions.ConnectionError:
            print("Erro ao atualizar proxies de thespeedx")

        try:
            for proxy in Repository.get_proxy_cz():
                test_proxy = Proxy(proxy.get("ip"), proxy.get("port"), proxy.get("kind"))
                self.testing_lane.append(test_proxy)
        except requests.exceptions.ConnectionError:
            print("Erro ao atualizar proxies de http://free-proxy.cz/")

        random.shuffle(self.testing_lane)

        with ThreadPoolExecutor(max_workers=200) as executor:
            executor.map(self.validate_proxies, self.testing_lane)


        #while len(self.testing_lane) > 0 and proxies
                
    def validate_proxies(self, proxy: Proxy, limit=100):
        try:
            if len(self.sessions) <= limit:
                proxy_s = proxy.get()
                session = requests.Session()
                response = session.get("https://api64.ipify.org/", timeout=10, proxies={"http": proxy_s, "https": proxy_s})
                session = Session(proxy)
                with self.lock:
                    self.add_session(session)
                    self.testing_lane.remove(proxy)
                print(f'Proxy {proxy.get()} validado. {len(self.sessions)}/{limit}({len(self.testing_lane)})')
        except requests.exceptions.Timeout as e:
            with self.lock:
                self.testing_lane.remove(proxy)
        except requests.exceptions.ConnectionError as e:
            with self.lock:
                self.testing_lane.remove(proxy)
            
    
    def __str__(self) -> str:
        return f'Existem no total {len(self.sessions)} proxies armazenados.'