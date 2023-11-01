import datetime
from entities.Proxy import Proxy
from threading import Thread, Lock

import requests

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
        proxy_ip = self.proxy.get()
        with self.lock:
            self.last_used = datetime.datetime.now()
        try:
            response = self.s.request("GET", url=url, params=params, timeout=timeout, proxies={"https": proxy_ip, "http": proxy_ip}, headers=headers)
            with self.lock:
                self.errors -= 1
            return response
        except Exception as e:
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
        return self.seconds_since_last_request() is None or self.seconds_since_last_request() > timeout

    def get_vivareal(self, page=0, amount=100, timeout=40):
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
        response = self.get("http://glue-api.vivareal.com/v2/listings", params=Params.get_vivareal_params(page, amount, 'São Paulo', 'Hortolândia'), headers=Repository.get_headers(self.proxy, 'www.vivareal.com.br'), timeout=timeout)
        
        serialized_json = response.json()

        return {
            "body": serialized_json["search"]["result"]["listings"],
            "page": serialized_json["page"]["uriPagination"],
        }
    
    
    def get_zap(self, page=0, amount=100, timeout=40):
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
        response = self.get("http://glue-api.zapimoveis.com.br/v2/listings", params=Params.get_vivareal_params(page, amount, 'São Paulo', 'Hortolândia'), headers=Repository.get_headers(self.proxy, 'https://www.zapimoveis.com.br'), timeout=timeout)
        
        serialized_json = response.json()

        return {
            "body": serialized_json["search"]["result"]["listings"],
            "page": serialized_json["page"]["uriPagination"],
        }