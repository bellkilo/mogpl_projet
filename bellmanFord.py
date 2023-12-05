from dictionnaireadjacenceorientepondere import DictionnaireAdjacenceOrientePondere
import math
from random import shuffle


"""
Sortie : plus_court_chemin, nb_iterations, bool_circuit_neg
"""
def BellmanFord(G, s):
    d = [math.inf for _ in range(G.nombre_sommets())]
    parent = [None for _ in range(G.nombre_sommets())]
    d[s] = 0
    parent[s] = s
    
    # parcourir |V|-1 fois
    for k in range(1, G.nombre_sommets()):
        converge = 1
        for v in G.sommets(): # parours de chaque sommet v
            lst_u = G.predecesseurs(v) # les sommets u tel que (u,v) est un arc dans G
            for u in lst_u: # parcours de tous les arcs entrants de v
                p = G.poids_arc(u, v)
                if d[u]+p < d[v]: # mise à jour de d[v] et de parent[v]
                    converge = 0 # il y a une modification donc pas de convergence   @ 
                    parent[v] = u
                    d[v] = d[u]+p
        if converge == 1: # convergence donc 
            return parent, k, 0
    
    # vérfication de la présence d'un circuit négatif
    for (u,v,p) in G.arcs(): # n-ième parcours de G
        if d[u]+p < d[v]:
            return parent, k, 1 # circuit négatif
    
    return parent, k, 0 # pas de circuit négatif


def BellmanFord2(G, s, ordre_sommets):
    d = [math.inf for _ in range(G.nombre_sommets())]
    parent = [None for _ in range(G.nombre_sommets())]
    d[s] = 0
    parent[s] = s
    
    # parcourir |V|-1 fois
    for k in range(1, G.nombre_sommets()):
        converge = 1
        for v in ordre_sommets: # parours de chaque sommet v
            lst_u = G.predecesseurs(v) # les sommets u tel que (u,v) est un arc dans G
            for u in lst_u: # parcours de tous les arcs entrants de v
                p = G.poids_arc(u, v)
                if d[u]+p < d[v]: # mise à jour de d[v] et de parent[v]
                    converge = 0 # il y a une modification donc pas de convergence    
                    parent[v] = u
                    d[v] = d[u]+p
        if converge == 1: # convergence donc 
            return parent, k, 0
    
    # vérfication de la présence d'un circuit négatif
    for (u,v,p) in G.arcs(): # n-ième parcours de G
        if d[u]+p < d[v]:
            return parent, k, 1 # circuit négatif
    
    return parent, k, 0 # pas de circuit négatif


def BellmanFordAleatoireUniforme(G, s):
    ordre = list(G.sommets())
    shuffle(ordre)
    print('ordre aléatoire: ', ordre)
    return BellmanFord2(G, s, ordre)



"""
Sortie : un sommet source, ou None s'il n'y en a pas
"""
def contient_source(G):
    for u in G.sommets():
        if G.degre_entrant(u) == 0:
            return u
    return None


"""
Sortie : un sommet puit, ou None s'il n'y en a pas
"""
def contient_puit(G):
    for u in G.sommets():
        if G.degre_sortant(u) == 0:
            return u
    return None


"""
On suppose que G n'est pas vide.

Sortie : un sommet u tel que ( deg_sort(u)-deg_entr(u) ) soit le maximum
"""
def max_diff_deg_sort_entr(G):
    maxi = 0
    res = list(G.sommets())[0]
    for u in G.sommets():
        tmp = G.degre_sortant(u) - G.degre_entrant(u)
        if maxi < tmp:
            maxi = tmp
            res = u
    return res


def GloutonFas(G):
    s1 = []
    s2 = []
    while G.nombre_sommets() != 0:
        
        u = contient_source(G)
        while u is not None:
            s1.append(u)
            G.retirer_sommet(u)
            u = contient_source(G)
        
        u = contient_puit(G)
        while u is not None:
            s2.insert(0, u)
            G.retirer_sommet(u)
            u = contient_puit(G)
        
        if G.nombre_sommets() != 0:
            u = max_diff_deg_sort_entr(G)
            s1.append(u)
            G.retirer_sommet(u)
    
    return s1+s2