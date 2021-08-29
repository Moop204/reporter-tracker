#!/usr/bin/env python3

from dotenv import load_dotenv
import json 
import os
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")
baseUrl = "https://api.newscatcherapi.com/v2/latest_headlines"
header={'x-api-key':API_KEY}


def loadJson(f): 
    content = json.load(f)
    # print(content)
    return content

def prepareData(): 
    res = []

    dataSrc1 = open('english_sources_1.json')
    res.append(json.load(dataSrc1))
    dataSrc1.close()  

    # dataSrc2 = open('english_sources_2.json')
    # res.append(json.load(dataSrc2))
    # dataSrc2.close()  

    # dataSrc3 = open('english_sources_3.json')
    # res.append(json.load(dataSrc3))
    # dataSrc3.close()  

    # dataSrc4 = open('english_sources_4.json')
    # res.append(json.load(dataSrc4))
    # dataSrc4.close()  

    # dataSrc5 = open('english_sources_5.json')
    # res.append(json.load(dataSrc5))
    # dataSrc5.close()  

    return res

    # # print(loadJson(dataSrc1))
    # mappedData = map(loadJson, [dataSrc1, dataSrc2, dataSrc3, dataSrc4, dataSrc5])

    # for elm in list(mappedData):
    #     print(elm)

    # # listData = list(mappedData)
    # print(mappedData[0])

def identifyEnglishPublishingCountries():
    loadedData = prepareData()
    angloPub = set()

    for data in loadedData: 
        for article in data['articles']: 
            angloPub.add(article['country'])
    return angloPub     

def requestPublicationsFromCountries(countries): 
    # for country in countries:
    country = countries.pop()
    publications = set()
    if(country != "unknown"):
        queries={'lang':'en', 'page_size':100, 'countries':[country]}
        # Enabled when used properly, limited calls
        # call = requests.get(baseUrl,headers=header, params=queries)
        # resp = json.load(call.text)
        # Sample output to save on API calls
        sampleFile = open('top_us.json')
        resp = json.load(sampleFile)
        sampleFile.close()
        for article in resp['articles']:
            publications.add(article['clean_url'])
    return list(publications)
        
def authorProfile(publications): 
    authorDict = {}
    # for publication in publications: 
    publication=publications[0]
    # Request headliners from publication
    queries={'lang':'en', 'page_size':100, 'page':1, 'sources':[publication]}
    # Enabled when used properly, limited calls
    # call = requests.get(baseUrl,headers=header, params=queries)    
    # Sample output to save on API calls
    sampleFile = open('author.json')
    resp = json.load(sampleFile)
    sampleFile.close()
    for article in resp['articles']: 
        articleTitle = article['title']
        source = article['clean_url']
        for author in article['authors']:
            if(author in authorDict):
                if(source in authorDict[author]):
                    authorDict[author][source].append(articleTitle)                    
                else: 
                    authorDict[author][source] = [articleTitle]
            else: 
                authorDict[author] = {source: [articleTitle] }

    print(authorDict)




angloCountries = identifyEnglishPublishingCountries()
publications = requestPublicationsFromCountries(angloCountries)
authorProfile(publications)


# dataSrc1.close()
# dataSrc2.close()
# dataSrc3.close()
# dataSrc4.close()
# dataSrc5.close()
