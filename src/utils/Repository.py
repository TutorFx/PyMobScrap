from typing import List
import requests
import random
import socket
import struct
import base64
from bs4 import BeautifulSoup
from entities.Empreendimento import Local, LocalContact
from entities.Proxy import Proxy, PremiumProxy
import os
from dotenv import load_dotenv

load_dotenv()

def get_ua():
    useragents: List[str] = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 ',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 ',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 ',
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577',
        'Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931',
        'Chrome (AppleWebKit/537.1; Chrome50.0; Windows NT 6.3) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.9200',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9',
        'Mozilla/5.0 (Linux; U; Android 2.3.5; zh-cn; HTC_IncredibleS_S710e Build/GRJ90) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.3.4; fr-fr; HTC Desire Build/GRJ22) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; T-Mobile myTouch 3G Slide Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.3.3; zh-tw; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.3.3; zh-tw; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari',
        'Mozilla/5.0 (Linux; U; Android 2.3.3; zh-tw; HTC Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.3.3; ko-kr; LG-LU3000 Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile',
        'Mozilla/5.0 (Linux; U; Android 2.3.3; de-de; HTC Desire Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.3.3; de-ch; HTC Desire Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.2; fr-lu; HTC Legend Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.2; en-sa; HTC_DesireHD_A9191 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.2.1; fr-fr; HTC_DesireZ_A7272 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.2.1; en-gb; HTC_DesireZ_A7272 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 2.2.1; en-ca; LG-P505R Build/FRG83) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
    ]
    return random.choice(useragents)

def generate_ip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

def get_proxy_blue():
    response = requests.get("https://free-proxy-list.net/", timeout=4)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    proxies = []
    rules = table.find_all('tr')
    for row in rules:
        columns = row.find_all('td')
        if columns:
            proxy = {
                'ip': columns[0].text,
                'port': columns[1].text,
                'kind': 'https' if columns[6].text == 'yes' else 'http'
            }
            proxies.append(Proxy(proxy.get("ip"), proxy.get("port"), proxy.get("kind")))
    return proxies

def get_froxy():
    proxies: List[PremiumProxy]  = []
    login = os.getenv('FROXY_LOGIN')
    password = os.getenv('FROXY_PASSWORD')
    for port in range(1000):
        proxies.append(PremiumProxy('fast.froxy.com', 10000 + port, "http", login, password))
        proxies.append(PremiumProxy('fast.froxy.com', 10000 + port, "socks5", login, password))
    return proxies


def get_proxy_cz():
    response = requests.get(
        "http://free-proxy.cz/en/proxylist/country/all/socks5/ping/all", timeout=4)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    rules = table.find_all('tr')
    for row in rules:
        columns = [e.text for e in row.find_all("td")]
        if len(columns) < 10:
            continue
        if columns:
            ip = row.find("script")
            ip = str(ip).split("(\"")[-1].split("\")")[0]
            ip = base64.b64decode(ip.encode("utf-8")).decode("utf-8")

            proxy = {
                'ip': ip,
                'port': columns[1],
                'kind': columns[2].lower()
            }
            proxies.append(Proxy(proxy.get("ip"), proxy.get("port"), proxy.get("kind")))
            
    return proxies

def get_headers(proxy: Proxy, origin: str):
    return {
        "x-domain": origin,
        "User-Agent": get_ua(),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json; charset=utf-8",
        "Referer": origin,
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",

        "x-forwarded-for": proxy.ip,
        "X-Originating-IP": proxy.ip,
        "X-Forwarded-For": proxy.ip,
        "X-Remote-IP": proxy.ip,
        "X-Remote-Addr": proxy.ip,
        "X-Client-IP": proxy.ip,
        "X-Host": proxy.ip,
        "X-Forwared-Host": proxy.ip,
    }


def get_thespeedx():
    methods = ['http', 'socks4', 'socks5']
    alldata = []

    def get_method(method):
        url = f"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/{method}.txt"
        response = requests.get(url, timeout=2)
        proxy_list = response.text.split('\n')
        proxies = []
        for proxy in proxy_list:
            proxy = proxy.split(':')
            proxies.append({
                'ip': proxy[0],
                'port': proxy[1],
                'kind': method
            })
        return proxies
    for method in methods:
        for proxy in get_method(method):
            alldata.append(Proxy(proxy.get("ip"), proxy.get("port"), proxy.get("kind")))
    return alldata

def glue_api_formatter(response):

    locais = []
    body = response.get("body", {})
    if not body:
        return locais
    for item in body:
        account = item.get("account", {})
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
    return locais