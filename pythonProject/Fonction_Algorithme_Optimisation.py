"""Ce fichier contient toutes les fonctions liées à la recherche du chemin optimale"""


import math
from Fonction_Modification_Graphe import *


#Cette fonction sert à trouer tous les chemins qui existe en tre deux villes en evitant les boucles
def trouver_tous_chemins(graphe, origine, extremite, visite=set(), chemin=[]):
    visite.add(origine)
    chemin = chemin + [origine]

    if origine == extremite:
        return [chemin]

    chemins = []

    for voisin in graphe.get(origine, {}):
        if voisin not in visite:
            nouveaux_chemins = trouver_tous_chemins(graphe, voisin, extremite, visite.copy(), chemin.copy())
            chemins.extend(nouveaux_chemins)

    return chemins



#cette fonction nous est servie pour la recherche des sommets ateignables depuis un sommet origine
def Successeur_Recurssive(graphe,origine, chemin_actuel=None):
    if chemin_actuel is None:
        chemin_actuel = [origine]

    if origine not in graphe or not graphe[origine]:
        return chemin_actuel
    if graphe[origine] == [()]:
         return
    for successeur in graphe[origine]:
        if successeur not in chemin_actuel:
            chemin_actuel.append(successeur)
            Successeur_Recurssive(graphe, successeur, chemin_actuel)

    return chemin_actuel

#foction pour determiner si un sommet est ateignable à partir d'un autre
def est_ateignable(origine,objectif,graphe):
    les_suivants=Successeur_Recurssive(origine,graphe)
    if objectif in les_suivants:
        return True
    return False

#cette fonction sert à retourner le poids direct entre deux sommets
#elle retourne le poids s'il existe un arret, et infini sinon
def distance(suivant,sommet1,sommet2):
    Suivants=suivant[sommet1]
    for sommet in Suivants:
        if sommet2 ==sommet[0]:
            return sommet[1]
    return math.inf
#de meme pour cette foncttion
def cout(suivant,sommet1,sommet2):
    Suivants = suivant[sommet1]
    for sommet in Suivants:
        if sommet2 == sommet[0]:
            return sommet[1]
    return math.inf

#Dijkstra, retourne la liste des distances et des precedents
def Dijkstra(racine, suivant):
    Sommets=les_sommet_de(suivant)

    ### initialisation ###
    L={}
    P={}
    M=[]
    L[racine]=0; #disatance entre la racine et la racine, c'est clair que c'est 0 (sans boucle)
    P[racine]=racine; #pour dire que j'ai passé de la racine à la racine

    SuivantRacine = suivant[racine] #pour enregistrer les suivants de la racine
    SommetSuivantRacine = [] #pour mettre tous les sommets qui sont suivants à la racine
    for a in SuivantRacine:
        SommetSuivantRacine.append(a[0])

    for sommet in Sommets: #parcours des restes de sommets
        if sommet in SommetSuivantRacine:
            L[sommet]= distance(suivant,racine,sommet) #retourner la distance entre le sommet racine et chaque sommet suivant
            P[sommet]= racine
        else:
            if sommet != racine: #pour eviter que le cas initial de la racine soit remplacé
                L[sommet]=math.inf #donner l'infinie comme distance pour cex qui ne sont pas suivant de la racine
                P[sommet]=""

    M.append(racine) #pour enregistrer la racine
    ### fin initialisation ###

    ###debut traintement ###
    while len(M) != len(Sommets):
        Sommet_restant=[]
        for x in Sommets: #pour rechercher les sommets qui ne sont pas enncore traité
            if x not in M:
                Sommet_restant.append(x)
        sommet_min=Sommet_restant[0]
        for y in Sommet_restant: #pour rechercher le sommet qui a la plus petite valeur dans L
            if L[sommet_min]>=L[y]:
                sommet_min=y
        if suivant[sommet_min] != [()]: ### pour eviter les sommets qui n'ont pas de suivant
            SuivantMP = suivant[sommet_min] #SuivantMP : suivant du minimium avec le poid
            SommetSuivantMin=[] #sommet suivant sans poid
            for z in SuivantMP:
                SommetSuivantMin.append(z[0]) #ajout des suivants du min dans SommetSuivantMin

            for SOMMET in Sommet_restant:
                if SOMMET in SommetSuivantMin:
                    if L[SOMMET]>L[sommet_min]+distance(suivant,sommet_min,SOMMET):
                        L[SOMMET]=L[sommet_min]+distance(suivant,sommet_min,SOMMET)
                        P[SOMMET]=sommet_min
        M.append(sommet_min)

    return L , P
    ### fin traitement ###

def Tous_Positive(suivant):
    verifie= True
    for sommet, suivant_sommet in suivant.items():
        if suivant_sommet != [()]:
            for Sommets in suivant_sommet:
                if Sommets[1] < 0:
                    verifie=False
                    return verifie
    return verifie

def PCC_Dijkstra(racine, extremite, suivant):
    # SuivantSpoid=Ignorer_poid(suivant)
    if Tous_Positive(suivant):
        L , P = Dijkstra(racine, suivant)
        chemin = [extremite]
        while racine not in chemin:
            ville_actuelle = P[chemin[-1]]
            chemin.append(ville_actuelle)
        chemin.reverse()
        return L[extremite] , chemin

#les deux fonctions suivantes seront utilisé quand je vais extraire la distance et le couts
#pour le Dijkstra dans le cas où on l'utilise sur la valeur
def temps_sur_un_chemin(chemin,graphe):
    temps=0
    for i in range(len(chemin)):
        if chemin[i]!=chemin[-1]:
            temps += distance(graphe,chemin[i],chemin[i+1])
    return temps

def couts_sur_un_chemin(chemin,graphe):
    couts=0
    for i in range(len(chemin)):
        if chemin[i] != chemin[-1]:
            couts += distance(graphe,chemin[i],chemin[i+1])
    return couts

#travaillons pour les cas où le voyageur veut passer par plusieurs villes de son choix
#fonction pour effectuer les calculs
def optimiser_le_parcours(graphe,Villes_a_visiter):
    chemin=[Villes_a_visiter[0]]
    ville_trouve=[Villes_a_visiter[0]]
    Visiter=Villes_a_visiter.copy()
    ville_a_explorer=Visiter[0]

    while len(ville_trouve)<len(Villes_a_visiter):
        minimum = math.inf
        Visiter.remove(ville_a_explorer)
        villes_a_etudier = Visiter

        for ville in villes_a_etudier:
            couts, x = PCC_Dijkstra(ville_a_explorer,ville,graphe)
            if minimum > couts:
                minimum = couts
                ville_a_explorer_suivante=ville
                chemin_trouve = x.copy()

        chemin_trouve.remove(ville_a_explorer)
        chemin.extend(chemin_trouve)
        ville_a_explorer=ville_a_explorer_suivante
        ville_trouve.append(ville_a_explorer)

    return chemin

def optimiser_le_parcours_aller_retour(graphe,Villes_a_visiter):
    chemin=[Villes_a_visiter[0]]
    ville_trouve=[Villes_a_visiter[0]]
    Visiter=Villes_a_visiter.copy()
    ville_a_explorer=Visiter[0]

    while len(ville_trouve)<len(Villes_a_visiter):
        minimum = math.inf
        Visiter.remove(ville_a_explorer)
        villes_a_etudier = Visiter

        for ville in villes_a_etudier:
            couts, x = PCC_Dijkstra(ville_a_explorer,ville,graphe)
            if minimum > couts:
                minimum = couts
                ville_a_explorer_suivante=ville
                chemin_trouve = x.copy()

        chemin_trouve.remove(ville_a_explorer)
        chemin.extend(chemin_trouve)
        ville_a_explorer=ville_a_explorer_suivante
        ville_trouve.append(ville_a_explorer)

    cout_retour , chemin_retour = PCC_Dijkstra(chemin[-1],chemin[0],graphe)
    chemin_retour.remove(chemin[-1])
    chemin.extend(chemin_retour)

    return chemin