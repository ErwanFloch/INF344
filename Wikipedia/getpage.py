#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode, unquote
import requests
import ssl
import itertools

global cache
cache = dict()

def getJSON(page):
    # here, page is not a html page but a key word !!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 2.1
    params = urlencode({
      'format': 'json',  # TODO: compléter ceci
      'action': 'parse',  # TODO: compléter ceci
      'prop': 'text',  # TODO: compléter ceci
      'redirects': 'true',  # TODO: compléter ceci
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"  # TODO: changer ceci
    # désactivation de la vérification SSL pour contourner un problème sur le
    # serveur d'évaluation -- ne pas modifier
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
   
    return response.read().decode('utf-8')


def getRawPage(page):
    # Ici non plus, page n'est pas une page html !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 2.2
    parsed = loads(getJSON(page))
    try:
        title = parsed['parse']['title']  # TODO: remplacer ceci
        content = parsed['parse']['text']['*']  # TODO: remplacer ceci
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        #print("La page demandée n'existe pas")
       return None, None

def correct_link(lien):
    
    # 4.2: decode non-ASCII 
    lien = unquote(lien)
    
    # 4.3
    if '#' in lien:
        index = lien.index('#')
        lien = lien[:index]
    
    #4.4
    lien = lien.replace('_', ' ')
    
    # 4.5
    if ':' in lien:
        lien = ''
    
    return lien
    
    
def getPage(page):
    page = unquote(page)
    #4.1
    if page in cache.keys():
        return page, cache[page]
    
    # 2.3
    try:
        title, content = getRawPage(page) # title = titre de la page après redirection
        title = unquote(title)
        # 2.3
        soup = BeautifulSoup(content, 'html.parser')
        soup = soup.find('div') # 2.4
        liens = []
        
        # 2.3  + 2.4
        for p in soup.find_all('p', recursive = False):
            for lien in p.find_all('a'):
                # 2.5 
                if (lien.get('href')[:6]=='/wiki/') and (lien.get('href')!=None):   # must not be None
                    # 2.6 + 4.3    
                    a = correct_link(lien.get('href')[6:])
                    if a != '' and a!=' ': # 4.3
                        liens.append(a)
        print('liens', liens)
        print('' )
        short_list = check_doublons(liens)
        print('short_list',  short_list)
        cache[title] = short_list
        cache[page] = short_list

    except:
        # 2.3
        return (None, [])
    
    # 2.7
    return title, short_list

def check_doublons(my_list):
    """

    Parameters
    ----------
    my_list : LIST.

    Returns
    -------
    b : BOOLEAN
        False si pas de doublon.

    """
    for e in my_list[:10]:
        ie = my_list.index(e)
        rest = my_list[ie + 1:]
        if e in rest:
            del my_list[ie]
    return my_list[:10]                      
                                  
test_list = ['bassin', 'velo', 'oiseau', 'coussin', 'oiseau', 'wagon', 'crayon', 'roue', 'train', 'oiseau', 'structure', 'camion', 'roulette']
    

if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    #print("Ça fonctionne !")
    #getJSON("Coronavirus")
    #print(getRawPage("Bonjour")[1])
    #print(getRawPage("bateau"))
    #print(getPage("lecture"))
    print(check_doublons(test_list))

    # Voici des idées pour tester vos fonctions :
    #print(getJSON("Utilisateur:A3nm/INF344"))
    #print(getRawPage("Utilisateur:A3nm/INF344"))
    #print(getPage("Utilisateur:A3nm/INF344"))
    # print(getRawPage("Histoire"))
    pass

