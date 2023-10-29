import time

class Proxy:
    def __init__(self, ip: str, port: str, type: str, time: float = time.time(), ):
        self.ip = ip
        self.port = port
        self.type = type
        self.time = time
    def __str__(self):
        return f'IP: {self.ip} e porta {self.port}'
    def get(self):
        return f'{self.type}://{self.ip}:{self.port}'