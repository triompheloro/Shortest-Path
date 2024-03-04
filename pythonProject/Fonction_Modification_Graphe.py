"""Ce fichier contient tous les fonctions qui consite à recuperer et manipuler
   les valeurs et la structure du graphe"""


#fonction pour importer le graphe depuis un fichier .txt
def importer_graphe(chemin_fichier):
    graphe = {}

    with open(chemin_fichier, 'r') as file:
        for ligne in file:
            sommet, voisins_part = ligne.strip().split(':')
            sommet = sommet.strip()

            if voisins_part:
                voisins = {}
                for voisin_part in voisins_part.split():
                    if '(' in voisin_part:
                        voisin, poids_part = voisin_part.split('(')
                        poids = tuple(map(int, poids_part[:-1].split(',')))
                    else:
                        voisin = voisin_part
                        poids = ()
                    voisins[voisin] = poids
            else:
                voisins = {}

            graphe[sommet] = voisins

    return graphe

#fonction pour creer une liste de tous les sommets du graphe
def les_sommet_de(graphe):
    sommets=[]
    for sommet in graphe.keys():
        sommets.append(sommet)
    return sommets

"""fonction pour construire un nouveua graphe derivé du graphe initialle en ne
considerant que les poids temps sur chaque arrets"""
def poids_temps(graphe):
    graphe_temps={}
    for sommet,suivant_sommets in graphe.items():
        graphe_temps[sommet]=[]
        for suivant,couts in suivant_sommets.items():
            time=couts[0]
            graphe_temps[sommet].append((suivant,time))
    for sommet,suivant_sommet in graphe_temps.items():
        if len(suivant_sommet)==0:
            graphe_temps[sommet]=[()]
    return graphe_temps

#De meme, ici, on ne considère que les poids couts
def poids_couts(graphe):
    graphe_temps = {}
    for sommet, suivant_sommets in graphe.items():
        graphe_temps[sommet] = []
        for suivant, couts in suivant_sommets.items():
            time = couts[1]
            graphe_temps[sommet].append((suivant, time))
    for sommet,suivant_sommet in graphe_temps.items():
        if len(suivant_sommet)==0:
            graphe_temps[sommet]=[()]
    return graphe_temps

"""Ici, nous avons fait la somme des deux (poid temps + poids cout) , comme 
nouvelle valeur de poid pour chaque arrets"""
def poids_temps_couts(graphe):
    graphe_temps = {}
    for sommet, suivant_sommets in graphe.items():
        graphe_temps[sommet] = []
        for suivant, couts in suivant_sommets.items():
            valeur = couts[1] + couts[0]
            graphe_temps[sommet].append((suivant,valeur))
    for sommet, suivant_sommet in graphe_temps.items():
        if len(suivant_sommet) == 0:
            graphe_temps[sommet] = [()]
    return graphe_temps

#cette fonction sert à lister les suivants de chaque sommet, en ignorant les poids
def Ignorer_poid(graphe): #pour enlever les poid, facilite la tache dans certain cas, ne travailler qu'avec les sommet
    Suivant_sans_poids={}
    for sommet in graphe:
        Suivant_sans_poids[sommet] = []
        if graphe[sommet] != [()]:
            for Suivants in graphe[sommet]:
                suivant=Suivants[0]
                if sommet in Suivant_sans_poids:
                    Suivant_sans_poids[sommet].append(suivant)
                else:
                    Suivant_sans_poids[sommet]=suivant
    return Suivant_sans_poids


