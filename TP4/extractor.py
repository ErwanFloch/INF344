'''Extracts type facts from a wikipedia file
usage: extractor.py wikipedia.txt output.txt

Every line of output.txt contains a fact of the form
    <title> TAB <type>
where <title> is the title of the Wikipedia page, and
<type> is a simple noun (excluding abstract types like
sort, kind, part, form, type, number, ...).

Note: the formatting of the output is already taken care of
by our template, you just have to complete the function
extractType below.

If you do not know the type of an entity, skip the article.
(Public skeleton code)'''

from parser import Parser
import sys
#import reimport 
import nltk

if len(sys.argv) !=3:
    print(__doc__)
    sys.exit(-1)

###########################################################################################################
# édiction de certaines règles
def extractType(content, title):
    # Code goes here
    mots_du_contenu = nltk.word_tokenize(content)
    contenu_tagging = nltk.pos_tag(mots_du_contenu)
    
    # tokenisation du titre
    mots_du_titre = []
    mots_du_titre = nltk.word_tokenize(title)
        
   # tag={word:tagg[1] for (word, tagg) in zip(words, tagging)}
    keywords =['way of', 'given to', 'part of', 'kind of', 'type of', 'sort of','name of', 'name for', 'one of', 'group of', 'shorter way', 'method of', 'form of', 'way of', 'way to', 'ways to', 'way for']
    aka = ['aka', 'a.k.a', 'also', 'also known as']
    
    # verbs
    verbs = ['VBZ', 'VBP', 'VBG', 'VBD']
    
    # noms
    nouns = ['NN', 'NNS', 'NNP', 'NNPS']
    
    typ = 'not defined'
  
    
    
    
    # si l'un des keyword de la liste keywords est présent dans le contenu, alors:
    if any(elem in content for elem in keywords):
        #index de ce mot dans le contenu:
        for elem in keywords:
            if elem in content:
                elem = elem[:-3]
                indice = content.index(elem)
                try:
                    typ = find_next_NN(content[indice+1 + len(elem):])
                except:
                       typ = 'A VOIR' 
                       
    elif any(elem in content for elem in aka):
        # on cherche le premier VBZ ou VBD, puis le dernier NN de la premiére liste de NN
        for elem in aka:
            if elem in content:
                indice = content.index(elem)
                try:
                    # on renvoie d'abord le permier verbe qui suit
                    verbe = find_next_VB(content[indice+1 + len(elem):])
                    # puis le dernier NN de la premiére liste de NN
                    indice = content.index(verbe)
                    typ = find_next_NN(content[indice+1 + len(verbe):])
                    
                except:
                       try:
                          typ = find_next_NN(content[indice+1 + len(elem):])
                       except:
                           typ = title[-1]         
    else:
        # si le contenu contient 1 mot ou 2, renvoyer le dernier mot
        if len(mots_du_contenu) < 3:
            typ = mots_du_contenu[:-1]
        
        # si tout le titre n'est pas dans le contenu
        if title not in content:
            # recherche du permier verbe
            try:
                verbe = [x for (x,y) in contenu_tagging if y in verbs][0]
                indice = content.index(verbe)
                typ = find_next_NN(content[indice+1 + len(verbe):])
            except:
                try:# on cherche, dans la sous-liste après le mot du titre présent dans le contenu, le dernier NN
                    nom = [x for (x,y) in contenu_tagging if y in nouns][0]
                    #indice = content.index(nom)
                    #typ = find_next_NN(content[indice+1 + len(nom):])
                    typ = nom
                except:
                    # on prend le premier NN qui ne soit pas dans le titre
                    try:
                        elem = [e for e in mots_du_contenu if e not in mots_du_titre][0]
                        indice = content.index(elem)
                        typ = find_next_NN(content[indice+1 + len(elem):])
                    except:
                        typ = mots_du_titre[0]
        
        else: #cas normal
            try: # on cherche le premier verbe, puis le dernier NN de la liste des NN après le dernier mot du titre
                verbe = find_next_VB(content)
                indice = content.index(verbe)
                typ = find_next_NN(content[indice+1 + len(verbe):])
            except: # on cherche le dernier NN de la liste des NN après le dernier mot du titre
                typ = title
                
         # 1er cas: le titre = CD
    if nltk.pos_tag(nltk.sent_tokenize(title))[0][1] == 'CD':
        # On cherche le premier verbe, puis le premier nom commun (plus exactement le dernier de la liste)
        try:
            verbe = find_next_VB(content) + ' '
            indice = content.index(verbe)
            typ = find_next_NN(content[indice+1 + len(verbe):])
            #typ = content[indice+1 + len(verbe):]
        except:    
            typ = content[0]
            
    return typ
###########################################################################################################
def find_next_NN(sous_liste):
    """
    Recherche les noms contenus dans la sous-liste donnée en argument et renvoie le dernier d'entre eux
    Ainsi, pour la sous-liste 'An American garden table', la fonction renverra table
    """

    # on determine les tags des mots de cette liste
    mots_du_contenu = nltk.word_tokenize(sous_liste)
    contenu_tagging = nltk.pos_tag(mots_du_contenu)
    
    accepted_nouns = ['NN', 'NNS', 'NNP', 'NNPS']
    
    # dans cette sous-liste, on cherche d'abord la position du prochain NN:
    result = [x for (x,y) in contenu_tagging if y in accepted_nouns ]
    
    # indice du premier nom
    indice = mots_du_contenu.index(result[0])
    
    # on recupere enfin tous les noms qui suivent
    res = []
    tag = contenu_tagging[indice][1]
    i = indice
    j = 0
    
    while tag in accepted_nouns:
        res.append(result[j])
        i += 1
        j += 1
        tag = contenu_tagging[i][1]
        
    # Enfin, on ne renvoie que le dernier élément de la liste
    return res[-1]  
    
###########################################################################################################
def find_next_VB(sous_liste):
    """
    renvoie le premier verbe contenu dans la sous-liste donnée en argument

    Parameters
    ----------
    sous_liste : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    # on determine les tags des mots de cette liste
    mots_du_contenu = nltk.word_tokenize(sous_liste)
    contenu_tagging = nltk.pos_tag(mots_du_contenu)
    
    accepted_verbs = ['VB', 'VBZ', 'VBD', 'VBP']
    
    # dans cette sous-liste, on cherche d'abord la liste des verbes:
    result = [x for (x,y) in contenu_tagging if y in accepted_verbs]
    
    # Puis, on renvoie le premier d'entre eux
    return result[0]


################################################################################
with open(sys.argv[2], 'w', encoding="utf-8") as output:
    print('startwikipedia-first.txt output.txt')
    for page in Parser(sys.argv[1]):
        typ = extractType(page.content, page.title)
        if typ:
            output.write(page.title + "\t" + typ + "\n")
    output.close