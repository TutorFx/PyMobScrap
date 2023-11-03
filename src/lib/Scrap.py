import os
from types import NoneType
from typing import List, Union
import requests
from entities.Empreendimento import Local, LocalContact, mock_local
from entities.Exceptions import NoValidData, NoValidProxies
from entities.Queue import Queue, QueueItem
from entities.Proxy import PremiumProxy, Proxy
from entities.Session import Session
import utils.Repository as Repository
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
import orjson
import random
import traceback

class GerenciadorDeLocais:
    def __init__(self):
        self.locais: List[Local] = [] # Este é o atributo que irá armazenar as instâncias de Local
        self.lock = Lock()
        self.storage = "./src/cache/locais.json"

    def add_local(self, local):
        with self.lock:
            if isinstance(local, Local):
                self.locais.append(local)
            else:
                print("Erro: o argumento deve ser uma instância da classe Local")

    def add_locais(self, locais: List[Local]):
        print(f"Adicionando {len(locais)} -> {len(self.locais) + len(locais)}")
        for local in locais:
            self.add_local(local)

        self.salvar_locais()

    def get_locais(self):
        print(f"Em um total existem {len(self.locais)} locais")
        return self.locais
    
    def carregar_locais(self):
        if not os.path.isfile(self.storage):
            # Se não existir, cria o arquivo
            with open(self.storage, 'w') as file: 
                file.write("[]")
        with open(self.storage, 'r') as file:
            locais_json = file.read()
            locais_dict = orjson.loads(locais_json)
            self.locais = [Local.from_dict(local_dict) for local_dict in locais_dict]
    
    def salvar_locais(self):
        with self.lock:
            if not os.path.isfile(self.storage):
                # Se não existir, cria o arquivo
                with open(self.storage, 'w') as file: 
                    file.write("[]")
            with open(self.storage, 'w') as file:
                locais_dict = [local.to_dict() for local in self.locais]
                locais_json = orjson.dumps(locais_dict)
                file.write(locais_json.decode())
    
    def __str__(self) -> str:
        return f'Existem no total {len(self.locais)} locais armazenados no Gerenciador.'


class ColetorDeLocais:
    cidade = None
    estado = None
    def __init__(self):
        self.gerenciador = GerenciadorDeLocais()
        self.proxy_collector = ProxyCollector()
        self.queue = Queue()

    def set_estado(self, estado):
        self.estado = estado

    def set_cidade(self, cidade):
        self.cidade = cidade

    def coletar_e_adicionar_locais(self, fonte):
        self.obter_locais(fonte)
        print(self.gerenciador.__str__())
    
    def obter_locais_v2(self, i: QueueItem):
        session = self.proxy_collector.get_random_session()
        if not isinstance(session, Session):
            print("Erro: não foi possível obter uma sessão válida")
            return;
    
        locais: List[Local] = []

        for _ in range(30):
            try: 
                if (i.origin == "vivareal"):
                    locais += session.get_vivareal(self.estado, self.cidade, i.page, i.amount)

                if (i.origin == "zap"):
                    locais += session.get_zap(self.estado, self.cidade, i.page, i.amount)
                
                print(f"Sucesso ao coletar dados de {i.origin}. ({session.errors}x de score) ({len(self.proxy_collector.sessions)}x Proxies ativos) ({len(locais)}x locais capturados)")
                
                if (len(locais) == 0):
                    print(f"Nenhum local foi encontrado para {i.origin}, p{i.page * i.amount} a{i.amount}")
                    raise NoValidData;
                return locais
            
            except requests.exceptions.ProxyError:
                print(f'Erro: Proxy {session.proxy.get()} não está disponível. Nenhuma conexão pôde ser feita porque a máquina de destino as recusou ativamente {i.origin} ({_})')
                # Obtenha uma nova sessão e tente novamente
                session = self.proxy_collector.get_random_session()
            except requests.exceptions.Timeout:
                print(f'Erro: {i.origin} demorou muito para responder ({_})')
                # Obtenha uma nova sessão e tente novamente
                session = self.proxy_collector.get_random_session()
            except requests.exceptions.ConnectionError:
                print(f'Erro: Ocorreu um erro ao se conectar com {i.origin} ({_})')
                # Obtenha uma nova sessão e tente novamente
                session = self.proxy_collector.get_random_session()
            except requests.exceptions.RequestException:
                print(f'Ocorreu um erro ao se conectar com {i.origin} ({_})')
                # Obtenha uma nova sessão e tente novamente
                session = self.proxy_collector.get_random_session()
            except NoValidProxies as e:
                print("Não existe nenhum proxy válido para a tarefa")
            except NoValidData as e:
                print("Não foi possível obter dados válidos")
            except Exception:
                traceback.print_exc()

    def enfileirar_locais(self, fonte, quantity = 10, amount = 100):
        print(f"Coletando locais de {fonte}")
        for page in range(quantity):
            self.queue.add_item(QueueItem(fonte, page, amount))
        random.shuffle(self.queue.items)

    def processar_fila(self, thread_n = 5):
        with ThreadPoolExecutor(max_workers=thread_n) as executor:
            futures = {executor.submit(self.obter_locais_v2, item) for item in self.queue.items}
            try:
                for future in as_completed(futures):
                    response = future.result()
                    if (isinstance(response, NoneType)):
                        print("Nenhum local foi retornado")
                        return;
                    self.gerenciador.add_locais(response)
            except Exception as e:
                print("An error occurred:", e.__repr__())
                traceback.print_exc()

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
            raise NoValidProxies("Não existem proxies válidos")
    
        # Ordena as sessões primeiro por disponibilidade (disponíveis primeiro) e depois por número de erros (menos erros primeiro)
        self.sessions.sort(key=lambda s: (-s.is_available(), s.errors, type(s.proxy) == PremiumProxy))
        # Remove da lista os piores proxies (com mais erros) e os melhores proxies que já fizeram +20 requisições bem sucedidas (com menos erros)
        self.sessions = list(filter(lambda s: s.errors <= 6 or s.errors >= -20 , self.sessions))
        
        available_sessions: List[Session] = [s for s in self.sessions if s.is_available()]
        unavailable_sessions: List[Session] = [s for s in self.sessions if not s.is_available()]

        if available_sessions:
            return available_sessions[0]
        else:
            return unavailable_sessions[0]  
    def scrap_proxies(self):
        """
        try:
            self.testing_lane += Repository.get_froxy()
        except requests.exceptions.ConnectionError:
            print("Erro ao atualizar de froxy")
        """
        try:
            self.testing_lane += Repository.get_proxy_blue()
        except requests.exceptions.ConnectionError:
            print("Erro ao atualizar proxies de http://free-proxy-list.net/")
        try:
            self.testing_lane += Repository.get_thespeedx()
        except requests.exceptions.ConnectionError:
            print("Erro ao atualizar proxies de thespeedx")

        try:
            self.testing_lane += Repository.get_proxy_cz()
        except requests.exceptions.ConnectionError:
            print("Erro ao atualizar proxies de http://free-proxy.cz/")
        random.shuffle(self.testing_lane)

        with ThreadPoolExecutor(max_workers=200) as executor:
            executor.map(self.validate_proxies, self.testing_lane)          
    def validate_proxies(self, proxy: Proxy, limit=50):
        try:
            if len(self.sessions) <= limit:
                proxy_s = proxy.get()
                session = requests.Session()
                session_created = Session(proxy)
                if (type(proxy) == PremiumProxy):
                    print(f'Proxy Premium {proxy.get()} furou a fila de testagem. {len(self.sessions)}/{limit}({len(self.testing_lane)})')
                    with self.lock:
                        self.add_session(session_created)
                        self.testing_lane.remove(proxy)
                    return; 
                session.get("https://api64.ipify.org/", timeout=10, proxies={"http": proxy_s, "https": proxy_s})
                with self.lock:
                    self.add_session(session_created)
                    self.testing_lane.remove(proxy)
                print(f'Proxy {proxy.get()} validado. {len(self.sessions)}/{limit}({len(self.testing_lane)})')
        except requests.exceptions.Timeout as e:
            with self.lock:
                self.testing_lane.remove(proxy)
        except requests.exceptions.ConnectionError as e:
            with self.lock:
                self.testing_lane.remove(proxy)
        except e:
            with self.lock:
                self.testing_lane.remove(proxy)
    
    def __str__(self) -> str:
        return f'Existem no total {len(self.sessions)} proxies armazenados.'