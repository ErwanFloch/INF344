usage='''
  Given as command line arguments
  (1) wikidataLinks.tsv 
  (2) wikidataLabels.tsv
  (optional 2') wikidataDates.tsv
  (3) wikipedia-ambiguous.txt
  (4) the output filename'''
'''writes lines of the form
        title TAB entity
  where <title> is the title of the ambiguous
  Wikipedia article, and <entity> is the 
  wikidata entity that this article belongs to. 
  It is OK to skip articles (do not output
  anything in that case). 
  (Public skeleton code)'''

import sys
import re
from parser2 import Parser
from simpleKB import SimpleKB
import nltk
import page


###########################################################################################################
def get_possible_entities(label):
    # renvoie le set associé au label
    return wikidata.rlabels[label]

###########################################################################################################
# premier algorithme
# on récupère la liste des entités possibles et on prend l'une des entités au hasard
def random_entity(label):
    entities_set = get_possible_entities(label) 
    return entities_set.pop()
###########################################################################################################
# deuxième algorithme
# on récupère l'ensemble des links de niveau 1 associès à un label
def Jaccard_premier_niveau(page):
    label = page.label()
    content = page.content
    
    possible_entities = get_possible_entities(label)
    
    # set des labels de la phrase
    Y = liste_NN(content)
    
    # ensemble des entités associées au label
    score = {}
    linked_entities_set = set()
    for entity in possible_entities:
        
        try:
            linked_entities_set = wikidata.links[entity]
        except (KeyError) as e:
            pass
        
        # ensemble de labels associés à l'entité
        labels_set = set()
        for entite in linked_entities_set:
            a = wikidata.labels[entite]
            for e in a:
                labels_set.add(e)
        
        # calcul du score de Jaccard
        score[entity] = jaccard(labels_set, Y)
        
    # tri des entites selon leur score
    a = sorted(score.items(), key=lambda t: t[1], reverse = True)
       
    return a[0][0]
###########################################################################################################
# troisième algorithme
# on récupère l'ensemble des links de niveau 1 et de niveau 2 associès à un label
def Jaccard_second_niveau(page):
    label = page.label()
    content = page.content
    
    possible_entities = get_possible_entities(label)
    
    # set des labels de la phrase
    Y = liste_NN(content)
    
    # ensemble des entités associées au label
    score = {}
    
    linked_entities_set1 = set()
    linked_entities_set2 = set()
    L1=list(linked_entities_set1)
    L2=[]
    for entity in possible_entities:
        linked_entities_set = set()    
        try:
            linked_entities_set1 = wikidata.links[entity]
           
            for ent in linked_entities_set1:
                linked_entities_set.add(ent)
           
            for entite in linked_entities_set1:
                try:
                    linked_entities_set2 = wikidata.links[entite]
                    for e in linked_entities_set2:
                        linked_entities_set.add(e)
                except (KeyError) as e:
                    pass 

        except (KeyError) as e:
            pass 
        
        # ensemble de labels associés à l'entité
        labels_set = set()
        for entit in linked_entities_set:
            a = wikidata.labels[entit]
            for e in a:
                labels_set.add(e)
        
        # calcul du score de Jaccard
        score[entity] = jaccard(labels_set, Y)
        
    # tri des entites selon leur score
    a = sorted(score.items(), key=lambda t: t[1], reverse = True)
       
    return a[0][0]
###########################################################################################################
# quatrième algorithme
# on récupère l'ensemble des links de niveau 2 associès à un label et uniquement ceux de niveau 2
def Jaccard_deuxieme_niveau(page):
    label = page.label()
    content = page.content
    
    possible_entities = get_possible_entities(label)
    
    # set des labels de la phrase
    Y = liste_NN(content)
    
    # ensemble des entités associées au label
    score = {}
    
    linked_entities_set1 = set()
    linked_entities_set2 = set()
    L1=list(linked_entities_set1)
    L2=[]
    for entity in possible_entities:
        linked_entities_set = set()    
        try:
            linked_entities_set1 = wikidata.links[entity]
                   
            for entite in linked_entities_set1:
                try:
                    linked_entities_set2 = wikidata.links[entite]
                    for e in linked_entities_set2:
                        linked_entities_set.add(e)
                except (KeyError) as e:
                    pass 

        except (KeyError) as e:
            pass 
        
        # ensemble de labels associés à l'entité
        labels_set = set()
        for entit in linked_entities_set:
            a = wikidata.labels[entit]
            for e in a:
                labels_set.add(e)
        
        # calcul du score de Jaccard
        score[entity] = jaccard(labels_set, Y)
        
    # tri des entites selon leur score
    a = sorted(score.items(), key=lambda t: t[1], reverse = True)
       
    return a[0][0]
###########################################################################################################
# cinquième algorithme
# on ne récupère pas l'ensemble des labels de la phrase mais seulement les noms propres
def Jaccard_cinquieme_methode(page):
    label = page.label()
    content = page.content
    
    possible_entities = get_possible_entities(label)
    
    # set des labels de la phrase
    try:
        Y = liste_NNP(content)
    except:
        Y = liste_NN(content)
        
    
    # ensemble des entités associées au label
    score = {}
    linked_entities_set = set()
    for entity in possible_entities:
        
        try:
            linked_entities_set = wikidata.links[entity]
        except (KeyError) as e:
            pass
        
        # ensemble de labels associés à l'entité
        labels_set = set()
        for entite in linked_entities_set:
            a = wikidata.labels[entite]
            for e in a:
                labels_set.add(e)
        
        # calcul du score de Jaccard
        score[entity] = jaccard(labels_set, Y)
        
    # tri des entites selon leur score
    a = sorted(score.items(), key=lambda t: t[1], reverse = True)
       
    return a[0][0]
###########################################################################################################
def Jaccard_sixieme_methode(page):
    label = page.label()
    content = page.content
    
    possible_entities = get_possible_entities(label)
    
    # set des labels de la phrase
    Y = liste_NN(content)
    
    # set des dates de la phrase
    Y_dates = liste_dates(content) 
    
    # ensemble des entités associées au label
    score = {}
    linked_entities_set = set()
    linked_dates_set = set()
    for entity in possible_entities:
        
        try:
            linked_entities_set = wikidata.links[entity]
        except (KeyError) as e:
            pass
        
        # ensemble de labels associés à l'entité
        labels_set = set()
        for entite in linked_entities_set:
            a = wikidata.labels[entite]
            for e in a:
                labels_set.add(e)
        
        
        # calcul du score de Jaccard combiné
        # dates associées à l'entité
        try:
            linked_dates_set = wikidata.dates[entity]
        except (KeyError) as e:
            pass
        
        # calcul du score de Jaccard
        try:
            score[entity] = jaccard(labels_set, Y) * (1+jaccard(linked_dates_set,Y_dates))
        except (ZeroDivisionError) as e:
            score[entity] = jaccard(labels_set, Y)
            
    # tri des entites selon leur score
    a = sorted(score.items(), key=lambda t: t[1], reverse = True)
       
    return a[0][0]
###########################################################################################################
def Jaccard_septieme_methode(page):
    label = page.label()
    content = page.content
    
    possible_entities = get_possible_entities(label)
    
    # set des labels de la phrase
    Y = liste_NN(content)
    
    # set des dates de la phrase
    Y_dates = liste_dates(content) 
    
    # ensemble des entités associées au label
    score = {}
    linked_entities_set = set()
    linked_dates_set = set()
    for entity in possible_entities:
        try:
            linked_dates_set = wikidata.dates[entity]
        except (KeyError) as e:
            pass
         
        if liste_dates(content)!= None and liste_dates(content) in linked_dates_set:
            return entity
        
        else:
            try:
                linked_entities_set = wikidata.links[entity]
            except (KeyError) as e:
                    pass
        
            # ensemble de labels associés à l'entité
            labels_set = set()
            for entite in linked_entities_set:
                a = wikidata.labels[entite]
                for e in a:
                   labels_set.add(e)
              
            # calcul du score de Jaccard
            score[entity] = jaccard(labels_set, Y)
            
            # tri des entites selon leur score
    a = sorted(score.items(), key=lambda t: t[1], reverse = True)
       
    return a[0][0]
###########################################################################################################
# liste des NN
# returns the liste of the nouns, supposed by me to be interesting labels
def liste_NN(content):
    content=content.replace('.','')
    accepted_nouns = ['NN', 'NNS', 'NNP', 'NNPS']
    a = nltk.pos_tag(nltk.word_tokenize(content))
    L = set()
    for e in a:
        if e[1] in accepted_nouns:
            L.add(e[0])
    return L
###########################################################################################################
# liste des NN
# returns the liste of the nouns, supposed by me to be interesting labels
def liste_NNP(content):
    content=content.replace('.','')
    accepted_nouns = ['NNP', 'NNPS']
    a = nltk.pos_tag(nltk.word_tokenize(content))
    L = set()
    for e in a:
        if e[1] in accepted_nouns:
            L.add(e[0])
    return L
###########################################################################################################
def find_first_NN(sous_liste):
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
        
        
    return set(res)
###########################################################################################################
def liste_dates(content):
# renvoie un set des dates contenues dans content
    # on determine les tags des mots de cette liste
    mots_du_contenu = nltk.word_tokenize(content)
    contenu_tagging = nltk.pos_tag(mots_du_contenu)
    dates = []
    for e in contenu_tagging:
        if e[1] == 'CD':
            dates.append(e[0])
    if dates !=[]:
        return dates[0]
    else:
        return None
###########################################################################################################
def jaccard(X,Y):
    
    # X_inter_Y
    X_inter_Y = set()
    for x in X:
        if x in Y:
            X_inter_Y.add(x)
    
    X_union_Y = set()
    for x in X:
        X_union_Y.add(x)
    for y in Y:    
         X_union_Y.add(y)   
    
    jaccard_score = len(X_inter_Y) / len(X_union_Y)
    return jaccard_score
###########################################################################################################
wikidata = None
if __name__ == "__main__":
    if len(sys.argv) is 5:
        dateFile = None
        wikipediaFile = sys.argv[3]
        outputFile = sys.argv[4]
    elif len(sys.argv) is 6:
        dateFile = sys.argv[3]
        wikipediaFile = sys.argv[4]
        outputFile = sys.argv[5]
    else:
        print(usage, file=sys.stderr)
        sys.exit(1)

    wikidata = SimpleKB(sys.argv[1], sys.argv[2], dateFile)
    print(type(wikidata.rlabels['Paris']))
# wikidata is here an object containing 4 dictionaries:
## wikidata.links is a dictionary of type: entity -> set(entity).
##                It represents all the entities connected to a
##                given entity in the yago graph
## wikidata.labels is a dictionary of type: entity -> set(label).
##                It represents all the labels an entity can have.
## wikidata.rlabels is a dictionary of type: label -> set(entity).
##                It represents all the entities sharing a same label.
## wikidata.dates is a dictionnary of type: entity -> set(date).
##                It represents all the dates associated to an entity.

# Note that the class Page has a method Page.label(),
# which retrieves the human-readable label of the title of an 
# ambiguous Wikipedia page.
###########################################################################################################
    


###########################################################################################################  


    with open(outputFile, 'w', encoding="utf-8") as output:
        for page in Parser(wikipediaFile):
 #           # DO NOT MODIFY THE CODE ABOVE THIS POINT
 #           # or you may not be evaluated (you can add imports).
        
            # YOUR CODE GOES HERE:
            #label = page.label()

            # 1er algorithme: on récupère l'une des entités au hasard => Grade: 14%
            #entity = random_entity(label)                            
            
            # 2ème algorithme: métrique de Jaccard au niveau 1 => Grade: 41%
            #entity = Jaccard_premier_niveau(page) 
            
            # 3ème algorithme: métrique de Jaccard au niveau 1 + 2
            #entity = Jaccard_second_niveau(page) 
            
            # 4ème algorithme: métrique de Jaccard au niveau 2
            #entity = Jaccard_deuxieme_niveau(page) 

            # 5ème algorithme: métrique de Jaccard au niveau 1 avec une sélection de labels de la phrase
            #entity = Jaccard_cinquieme_methode(page) 
            
            # 6ème algorithme: métrique de Jaccard au niveau 1  + dates
            #entity = Jaccard_sixieme_methode(page) 
            
            # 7ème algorithme: métrique de Jaccard au niveau 1  + dates
            entity = Jaccard_septieme_methode(page)
            #
            output.write(page.title+"\t"+entity+"\n")
