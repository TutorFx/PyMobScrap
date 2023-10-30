from entities.Proxy import Proxy

import requests
#from http.cookies import MozillaCookieJar

import utils.Repository as Repository
import utils.Params as Params

class Session:
    errors = 0;

    def __init__(self, proxy: Proxy):        
        self.proxy = proxy;
        self.s = requests.Session()
        #self.cj = MozillaCookieJar()
        self.s.cookies = self.cj
        self.s.headers = Repository.get_headers(proxy)
        
    def get(self, url: str, params: object, timeout=20):
        proxy_ip = self.proxy.get()
        self.s.request("GET", url=url, params=params, timeout=timeout, proxies={"https": proxy_ip, "http": proxy_ip})

    def get_vivareal(self, page=0, amount=100):
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
        response = self.s.get("http://glue-api.vivareal.com/v2/listings", params=Params.get_vivareal_params(page=page, amount=amount))

        serialized_json = response.json()

        return {
            "body": serialized_json["search"]["result"]["listings"],
            "page": serialized_json["page"]["uriPagination"],
        }