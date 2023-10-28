import requests
def get_vivareal_data(page=0, amount=100):
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
  url = "https://glue-api.vivareal.com/v2/listings"
  headers = {
    "x-domain": "www.vivareal.com.br",
  }
  querystr = {
    "business":"RENTAL",
    "facets":"amenities",
    "unitTypes":"",
    "unitSubTypes":"",
    "unitTypesV3":"",
    "usageTypes":"",
    "listingType":"USED",
    "parentId":"null",
    "categoryPage":"RESULT",
    "includeFields":"search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount),page,seasonalCampaigns,fullUriFragments,nearby(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount)),expansion(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount)),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier,phones),owners(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount))",
    "size":str(amount),
    "from":str(page * amount),
    "q":"",
    "developmentsSize":"5",
    "__vt":"control",
    "levels":"LANDING",
    "ref":"",
    "pointRadius":"",
    "isPOIQuery":""
  }
  session = requests.Session();
  session.headers = headers
  session.params = querystr
  response = session.request("GET", url);
  print(response.status_code)
  serialized_json = response.json();
  
  return {
    "body": serialized_json["search"]["result"]["listings"],
    "page": serialized_json["page"]["uriPagination"],
  };