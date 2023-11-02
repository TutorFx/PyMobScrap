import time

class Proxy:
    def __init__(self, ip: str, port: str, kind: str, time: float = time.time(), ):
        self.ip = ip
        self.port = port
        self.kind = kind
        self.time = time
    def __str__(self):
        return f'IP: {self.ip} e porta {self.port}'
    def get(self):
        return f'{self.kind}://{self.ip}:{self.port}'

class PremiumProxy(Proxy):
    def __init__(self, ip: str, port: str, kind: str, login: str, password: str, time: float = time.time()):
       self.login = login
       self.password = password
       super().__init__(ip, port, kind, time)
    def get(self):
        return f'{self.kind}://{self.login}:{self.password}@{self.ip}:{self.port}'