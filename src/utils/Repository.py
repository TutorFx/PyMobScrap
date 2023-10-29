import requests
import random
import socket
import struct
import base64
from bs4 import BeautifulSoup
from entities.Proxy import Proxy



def generate_ip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))


def get_free_proxy_list_net():
    response = requests.get("https://free-proxy-list.net/", timeout=2)
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
              'type': 'https' if columns[6].text == 'yes' else 'http'
            }
            proxies.append(proxy)
    return proxies

def get_free_proxy_cz():
    response = requests.get("http://free-proxy.cz/en/proxylist/country/all/socks5/ping/all", timeout=2)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    rules = table.find_all('tr')
    print('passou')
    for row in rules:
        columns = [e.text for e in row.find_all("td")]
        if len(columns) < 10:
            continue
        if columns:
            ip = row.find("script")
            ip = str(ip).split("(\"")[-1].split("\")")[0]
            ip = base64.b64decode(ip.encode("utf-8")).decode("utf-8")
            print(ip)

            proxy = {
              'ip': ip,
              'port': columns[1],
              'type': columns[2].lower()
            }
            print(proxy)
            proxies.append(proxy)
    return proxies


def get_vivareal_data(proxy: Proxy, page=0, amount=100):
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
    ip = generate_ip()
    url = "http://glue-api.vivareal.com/v2/listings"
    headers = {
        "x-domain": "www.vivareal.com.br",

        "x-forwarded-for": ip,
        "X-Originating-IP": ip,
        "X-Forwarded-For": ip,
        "X-Remote-IP": ip,
        "X-Remote-Addr": ip,
        "X-Client-IP": ip,
        "X-Host": ip,
        "X-Forwared-Host": ip,
    }
    querystr = {
        "business": "RENTAL",
        "facets": "amenities",
        "unitTypes": "",
        "unitSubTypes": "",
        "unitTypesV3": "",
        "usageTypes": "",
        "listingType": "USED",
        "parentId": "null",
        "categoryPage": "RESULT",
        "includeFields": "search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount),page,seasonalCampaigns,fullUriFragments,nearby(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount)),expansion(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount)),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier,phones),owners(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount))",
        "size": str(amount),
        "from": str(page * amount),
        "q": "",
        "developmentsSize": "5",
        "__vt": "control",
        "levels": "LANDING",
        "ref": "",
        "pointRadius": "",
        "isPOIQuery": ""
    }
    session = requests.Session()
    session.headers = headers
    session.params = querystr
    response = session.request("GET", url, proxies={ "http": proxy.get() })
    print(response.status_code)
    serialized_json = response.json()

    return {
        "body": serialized_json["search"]["result"]["listings"],
        "page": serialized_json["page"]["uriPagination"],
    }
