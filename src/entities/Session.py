import datetime
from types import NoneType
from typing import List
import orjson
import requests
from entities.Exceptions import NoValidProxies
from entities.Proxy import Proxy
from threading import Thread, Lock
from entities.Empreendimento import Local
import orjson
import requests
import json

import utils.Repository as Repository
import utils.Params as Params

class Session:
    errors = 0;
    last_used = None;

    def __init__(self, proxy: Proxy):        
        self.proxy = proxy;
        self.s = requests.Session()
        self.lock = Lock()
        
    def get(self, url: str, params: object, headers, timeout=40):
        with self.lock:
            self.last_used = datetime.datetime.now()
        try:
            proxy_ip = self.proxy.get()
            response = self.s.request("GET", url=url, params=params, timeout=timeout, proxies={"https": proxy_ip, "http": proxy_ip}, headers=headers)
            print("Sucesso!")
            with self.lock:
                self.errors -= 1
            return response
        except requests.exceptions.ProxyError as e:
            with self.lock:
                self.errors += 1
            raise e
        except requests.exceptions.Timeout as e:
            with self.lock:
                self.errors += 1
            raise e
        except requests.exceptions.RequestException as e:
            with self.lock:
                self.errors += 1
            raise e
        except NoValidProxies as e:
            with self.lock:
                self.errors += 1
            raise e
        finally:
            print(f'Proxy {proxy_ip} com {self.errors} erros.')

    def seconds_since_last_request(self):
        if self.last_used is None:
            return None
        return (datetime.datetime.now() - self.last_used).total_seconds()

    def is_available(self, timeout=40):
        return self.seconds_since_last_request() is None or self.seconds_since_last_request() > timeout + 3

    def get_vivareal(self, estado, cidade, page=0, amount=100, timeout=40):
        """
        Essa função espera dois argumentos, o `page` e o `amount`\n
        Arguments:\n
            page: inteiro
            amount: inteiro
        Returns:\n
        ```  
          "body": ...["search"]["result"]["listings"],
          "page": ...["page"]["uriPagination"],
        ```
        """
        response = self.get("http://glue-api.vivareal.com/v2/listings", params=Params.get_vivareal_params(
            page, amount, estado, cidade), headers=Repository.get_headers(self.proxy, 'www.vivareal.com.br'), timeout=timeout)
        
        if (response.status_code == 400):
            print(response.text)
        
        serialized_json = json.loads(response.text)

        if (isinstance(serialized_json, NoneType)):
            return []

        formatted = {
            "body": serialized_json.get('search', {}).get('result', {}).get('listings', None),
            "page": serialized_json.get('page', {}).get('uriPagination', {}),
        }

        locais: List[Local] = []
        for local in Repository.glue_api_formatter(formatted, 'Vivareal'):
            locais.append(local)

        return locais

    def get_zap(self, estado, cidade, page=0, amount=100, timeout=40):
        """
        Essa função espera dois argumentos, o `page` e o `amount`\n
        Arguments:\n
            page: inteiro
            amount: inteiro
        Returns:\n
        ```  
          "body": ...["search"]["result"]["listings"],
          "page": ...["page"]["uriPagination"],
        ```
        """
        response = self.get("http://glue-api.zapimoveis.com.br/v2/listings", params=Params.get_vivareal_params(page, amount,
                            estado, cidade), headers=Repository.get_headers(self.proxy, 'https://www.zapimoveis.com.br'), timeout=timeout)
        if (response.status_code == 400):
            print(response.text)
        
        serialized_json = json.loads(response.text)

        if (isinstance(serialized_json, NoneType)):
            print(response, page, amount)
            return []
        
        formatted = {
            "body": serialized_json.get('search', {}).get('result', {}).get('listings', None),
            "page": serialized_json.get('page', {}).get('uriPagination', {}),
        }

        print(formatted["page"])

        locais: List[Local] = []

        for local in Repository.glue_api_formatter(formatted, "Zap"):
            locais.append(local)

        return locais
