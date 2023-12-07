from dictionnaireadjacenceorientepondere import DictionnaireAdjacenceOrientePondere
import math
import random
from bellmanFord import BellmanFord


def generer_graphe(n):
    G = DictionnaireAdjacenceOrientePondere()
    G.ajouter_sommets([i for i in range(n)])

    source = random.randint(0, n-1)
    
    sommets_accessible = set()
    sommets_accessible.add(source)

    while len(sommets_accessible) <= n/2:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if v != u and v not in G.successeurs(u):
            poids = random.randint(-10, 10)
            G.ajouter_arc(u, v, poids)
            if u in sommets_accessible:
                sommets_accessible.add(v)

    for u in G.sommets():
        out_edges = G.degre_sortant(u)
        while out_edges < 5:
            v = random.randint(0, n-1)
            if v != u and v not in G.successeurs(u):
                poids = random.randint(-10, 10)
                G.ajouter_arc(u, v, poids)
                out_edges += 1
    
    
    
    print("source:", source)
    return G, source


def generer_homographe(G):
    H = DictionnaireAdjacenceOrientePondere()
    H.ajouter_sommets(G.sommets())
    for (u,v,p) in G.arcs():
        w = random.randint(-10, 10)
        H.ajouter_arc(u,v,w)
    return H
    

def union_chemin(G1, G2, G3, s):
    graphe = DictionnaireAdjacenceOrientePondere()
    graphe.ajouter_sommets(G1.sommets())
    
    chemin1, _, _ = BellmanFord(G1, s)
    chemin2, _, _ = BellmanFord(G2, s)
    chemin3, _, _ = BellmanFord(G3, s)
    print(chemin1)
    print(chemin2)
    print(chemin3)
    for u in range(len(chemin1)):
        if u == chemin1[u] :
            continue
        if chemin1[u] is not None:
            graphe.ajouter_arc(chemin1[u], u, 1)
        if chemin2[u] is not None and u not in graphe.successeurs(chemin2[u]):
            graphe.ajouter_arc(chemin2[u], u, 1)
        if chemin3[u] is not None and u not in graphe.successeurs(chemin3[u]):
            graphe.ajouter_arc(chemin3[u], u, 1)
    return graphe

def union_chemin_iter(lst_G, s):
    H = DictionnaireAdjacenceOrientePondere()
    if len(lst_G) > 0:
        H.ajouter_sommets(lst_G[0].sommets())
        for i in range(len(lst_G)):
            chemin, _,_ = BellmanFord(lst_G[i], s)
            for v in range(len(chemin)):
                u = chemin[v]
                if u == v:
                    continue # pas de boucle
                if u is not None and v not in H.successeurs(u):
                    H.ajouter_arc(u, v, 1)
    return H

if __name__ == '__main__':
    while True:
        g, s = generer_graphe(8)
        parent, k, isNegatif = BellmanFord(g, s)
        if isNegatif == 0:
            break


    print(g)
    file = open('graphe.txt', 'w')
    g.saveGraph(file, s)
    file.close()

    while True:
        G1 = generer_homographe(g)
        parent, k, isNegatif = BellmanFord(G1, s)
        if isNegatif == 0:
            break
    file = open('graphe1.txt', 'w')
    G1.saveGraph(file, s)
    file.close()


    while True:
        G2 = generer_homographe(g)
        parent, k, isNegatif = BellmanFord(G2, s)
        if isNegatif == 0:
            break
    file = open('graphe2.txt', 'w')
    G2.saveGraph(file, s)
    file.close()

    while True:
        G3 = generer_homographe(g)
        parent, k, isNegatif = BellmanFord(G3, s)
        if isNegatif == 0:
            break
    file = open('graphe3.txt', 'w')
    G3.saveGraph(file, s)
    file.close()