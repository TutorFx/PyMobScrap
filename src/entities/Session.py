from entities.Proxy import Proxy

import cloudscraper
import requests

import utils.Repository as Repository
import utils.Params as Params

class Session:
    errors = 0;

    def __init__(self, proxy: Proxy):        
        self.proxy = proxy;
        self.s = requests.Session()

        
    def get(self, url: str, params: object, headers, timeout=40):
        proxy_ip = self.proxy.get()
        return self.s.request("GET", url=url, params=params, timeout=timeout, proxies={"https": proxy_ip, "http": proxy_ip}, headers=headers)
        

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