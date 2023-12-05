from dictionnaireadjacenceorientepondere import DictionnaireAdjacenceOrientePondere
import math
import random
import copy


"""
Sortie : plus_court_chemin, nb_iterations, bool_circuit_neg
"""
def BellmanFord(G, s):
    # print("BF START")
    d = [math.inf for _ in range(G.nombre_sommets())]
    parent = [None for _ in range(G.nombre_sommets())]
    d[s] = 0
    parent[s] = s
    
    ## parcourir |V|-1 fois
    for k in range(1, G.nombre_sommets()):
        converge = 1
        for v in G.sommets(): # parours de chaque sommet v dans l'ordre croissant
            lst_y = G.predecesseurs(v) # les sommets y tel que (y,v) est un arc dans G
            for y in lst_y: # parcours de tous les arcs entrants de v
                w = G.poids_arc(y, v)
                if d[y]+w < d[v]: # mise à jour de d[v] et de parent[v]
                    # print("distance:", d)
                    # print("parent:", parent)
                    # print("y:", y, "| v:", v)
                    converge = 0 # il y a une modification donc pas de convergence    
                    parent[v] = y
                    d[v] = d[y]+w
        if converge == 1: # convergence donc 
            return parent, k
    
    ## vérification de la présence d'un circuit négatif
    for (u,v,p) in G.arcs(): # n-ième parcours de G
        if d[u]+p < d[v]:
            print("distance:", d)
            print("parent:", parent)
            print("u:", u, "| v:", v)
            print("Circuit négatif !")
            exit(1)
            return parent, k # circuit négatif
    
    return parent, k


def BellmanFord2(G, s, ordre_sommets):
    # print("BF START")
    d = [math.inf for _ in range(G.nombre_sommets())]
    parent = [None for _ in range(G.nombre_sommets())]
    d[s] = 0
    parent[s] = s
    
    ## parcourir |V|-1 fois
    for k in range(1, G.nombre_sommets()):
        converge = 1
        for v in ordre_sommets: # parours de chaque sommet v dans l'ordre trouvé par GloutonFas
            lst_y = G.predecesseurs(v) # les sommets y tel que (y,v) est un arc dans G
            for y in lst_y: # parcours de tous les arcs entrants de v
                w = G.poids_arc(y, v)
                if d[y]+w < d[v]: # mise à jour de d[v] et de parent[v]
                    # print("distance:", d)
                    # print("parent:", parent)
                    # print("y:", y, "| v:", v)
                    converge = 0 # il y a une modification donc pas de convergence    
                    parent[v] = y
                    d[v] = d[y]+w
        if converge == 1: # convergence donc 
            return parent, k
    
    ## vérfication de la présence d'un circuit négatif
    for (u,v,p) in G.arcs(): # n-ième parcours de G
        if d[u]+p < d[v]:
            print("distance:", d)
            print("parent:", parent)
            print("u:", u, "| v:", v)
            print("Circuit négatif !")
            exit(1)
            return parent, k # circuit négatif
    
    return parent, k


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


def ancetres(G, u, res):
    if res == []:
        res = list(G.predecesseurs(u))
    #print("res init:", res)
    taille_avant = len(res)
    nouv_pred = []
    for x in res:
        #print("u:", u)
        nouv_pred += list(G.predecesseurs(x))
    res += nouv_pred
    res = list(set(res)) # enlever les doublons
    #print("res 1er trait:", res)
    if taille_avant != len(res): # il y a de nouveaux ancêtres
        res = list(ancetres(G, u, res))
    #print("res final:", res)
    return set(res)


def descendants(G, v, res):
    if res == []:
        res = list(G.successeurs(v))
    #print("res init:", res)
    taille_avant = len(res)
    nouv_succ = []
    for y in res:
        #print("v:", v)
        nouv_succ += list(G.successeurs(y))
    res += nouv_succ
    res = list(set(res)) # enlever les doublons
    #print("res 1er trait:", res)
    if taille_avant != len(res): # il y a de nouveaux descendants
        res = list(descendants(G, v, res))
    #print("res final:", res)
    return set(res)


def generer_graphe(n, p):
    cmp = n
    ## Initialisation
    G = DictionnaireAdjacenceOrientePondere()
    G.ajouter_sommets([i for i in range(n)])

    source = random.randint(0,n-1)
    ancetre = [i for i in range(n)]
    distance = [[math.inf]*G.nombre_sommets() for _ in range(G.nombre_sommets())] # distance min
    # for i in range(G.nombre_sommets()):
    #     distance[i][i] = 0

    while ancetre.count(source) <= n/2:
        # prend trop de temps, on efface tout et on recommence
        if cmp > n:
            cmp = 0
            ## Nouvelle initialisation
            G = DictionnaireAdjacenceOrientePondere()
            G.ajouter_sommets([i for i in range(n)])

            source = random.randint(0,n-1)
            ancetre = [i for i in range(n)]
            distance = [[math.inf]*G.nombre_sommets() for _ in range(G.nombre_sommets())] # distance min
            # for i in range(G.nombre_sommets()):
            #     distance[i][i] = 0

        ## Traitement d'ajout d'arcs
        for u in G.sommets():
            for v in G.sommets():
                if u != v and G.poids_arc(u,v) is None: # ni boucle ni plusieurs arcs directs de u à v
                    q = random.random()
                    if q < p: # proba p d'avoir un arc de u vers v
                        poids = random.randint(-10,10)
                        circuit_neg = 0
                        ## Détection de différents cas de circuit absorbant
                        if distance[v][u] + poids < 0:
                            circuit_neg = 1
                        for x in G.sommets():
                            if x != u and x != v:
                                if distance[x][u] + poids + distance[v][x] < 0:
                                    circuit_neg = 1 
                        # for x in ancetres(G, u, []):
                        #     # if x != u and x != v:
                        #         if distance[x][u] + poids + distance[v][x] < 0:
                        #             circuit_neg = 1
                        # for y in descendants(G, v, []):
                        #     # if y != u and y != v:
                        #         if distance[y][u] + poids + distance[v][y] < 0:
                        #             circuit_neg = 1
                        # pas de circuit négatif --> ajout de l'arc et mise à jour des distances min
                        if circuit_neg == 0: 
                            distance[u][v] = min(distance[u][v], poids)
                            ancetre[v] = ancetre[u]
                            G.ajouter_arc(u,v,poids)

                            # for x in G.sommets():
                            #     if x != u:
                            #         distance[x][v] = min(distance[x][v], distance[x][u] + poids)
                            #     if x != v:
                            #         distance[u][x] = min(distance[u][x], poids + distance[v][x])

                            pred_tot = list(G.predecesseurs(u)) # pred proche (début liste) à pred éloigné (fin liste)
                            pred_i = list(G.predecesseurs(u))
                            while len(pred_i) != 0:
                                pred_i_1 = []
                                for x1 in pred_i: # parcours de tous les prédecesseurs actuels
                                    for x2 in G.predecesseurs(x1): # parcours de tous les prédecesseurs du prédecesseur actuel
                                        if x2 not in pred_tot: # si le prédecesseur n'est pas encore dans la liste, on l'ajoute
                                            pred_i_1.append(x2)
                                pred_tot += pred_i_1 # concaténation des listes de prédecesseurs
                                pred_i = pred_i_1
                            
                            succ_tot = list(G.successeurs(v)) # pred proche (début liste) à pred éloigné (fin liste)
                            succ_i = list(G.successeurs(v))
                            while len(succ_i) != 0:
                                succ_i_1 = []
                                for y1 in succ_i: # parcours de tous les prédecesseurs actuels
                                    for y2 in G.successeurs(y1): # parcours de tous les prédecesseurs du prédecesseur actuel
                                        if y2 not in succ_tot: # si le prédecesseur n'est pas encore dans la liste, on l'ajoute
                                            succ_i_1.append(y2)
                                succ_tot += succ_i_1 # concaténation des listes de prédecesseurs
                                succ_i = succ_i_1
                            
                            # succ_i = G.successeurs(v)
                            # while len(succ_i) != 0: # mise à jour du descendant le plus proche de v jusqu'au plus éloigné
                            #     succ_i_1 = set()
                            #     for y in succ_i:
                            #         if distance[u][y] > poids + distance[v][y]:
                            #             # print(G)
                            #             # print("u:", u, "v:", v, "y:", y)
                            #             distance[u][y] = poids + distance[v][y]
                            #             succ_i_1 |= G.successeurs(y)
                            #     succ_i = succ_i_1
                            
                            # changement = 1
                            # while changement == 1:
                            #     changement = 0
                            #     for x in pred_tot: # x --> u --> v
                            #         if distance[x][v] > distance[x][u] + poids:
                            #             distance[x][v] = distance[x][u] + poids
                            #             changement = 1
                            #     for y in succ_tot: # u --> v --> y
                            #         if distance[u][y] > poids + distance[v][y]:
                            #             distance[u][y] = poids + distance[v][y]
                            #             changement = 1
                            #     for z in G.sommets():
                            #         if z != u and z != v: # u --> z --> v
                            #             if distance[u][v] > distance[u][z] + distance[z][v]:
                            #                 distance[u][v] = distance[u][z] + distance[z][v]
                            #                 changement = 1

                            changement = 1
                            while changement == 1:
                                changement = 0
                                for z in G.sommets():
                                    for y in G.sommets():
                                        for x in G.sommets():
                                            if distance[u][v] > distance[u][z] + distance[z][v]:
                                                distance[u][v] = distance[u][z] + distance[z][v]
                                                changement = 1
                                            if distance[z][v] > distance[z][u] + poids:
                                                distance[z][v] = distance[z][u] + poids
                                                changement = 1
                                            if distance[u][z] > poids + distance[v][z]:
                                                distance[u][z] = poids + distance[v][z]
                                                changement = 1
                                            if x != y and y != z and x != z:
                                                if distance[x][z] > distance[x][y] + distance[y][z]:
                                                    distance[x][z] = distance[x][y] + distance[y][z]
                                                    changement = 1
                                
                            
                            # while len(pred_tot) != 0:
                            #     x = pred_tot.pop()
                            #     if distance[x][v] > distance[x][u] + poids:
                            #         distance[x][v] = distance[x][u] + poids

                            # while len(pred_tot) != 0: # mise à jour de l'ancêtre le plus éloigné de u jusqu'au plus proche
                            #     pred_i_1 = set()
                            #     for x in pred_i:
                            #         if distance[x][v] < distance[x][u] + poids:
                            #             print(G)
                            #             print("x:", x, "u:", u, "v:", v)
                            #             distance[x][v] = distance[x][u] + poids
                            #             pred_i_1 |= G.predecesseurs(x)
                            #     pred_i = pred_i_1
                            


                            # for x in ancetres(G, u, []):
                            #     if x != u and x != v:
                            #         distance[x][v] = min(distance[x][v], distance[x][u] + poids)
                            # for y in descendants(G, v, []):
                            #     if y != u and y != v:
                            #         distance[u][y] = min(distance[u][y], poids + distance[v][y])
                            
                            # for x in G.sommets():
                            #     if x != u and x != v:
                            #         if distance[x][u] != math.inf: # mise à jour de la distance min de x -> u -> v
                            #             distance[x][v] = min(distance[x][v], distance[x][u] + poids)
                            #         if distance[v][x] != math.inf: # mise à jour de la distance min de u -> v -> x
                            #             distance[u][x] = min(distance[u][x], poids + distance[v][x])

        cmp += 1
    # print("ancetre:", ancetre)
    return G, source

                
"""
Sortie : un graphe H, avec les mêmes arcs, mais de poids différents que ceux du graphe d'entrée G
"""
def generer_homographe(G):
    graphe_ok = 0
    n = G.nombre_sommets()

    while True:
        ## (Nouvelle) Initialisation
        graphe_ok = 1
        H = DictionnaireAdjacenceOrientePondere()
        H.ajouter_sommets(G.sommets())

        distance = [[math.inf]*H.nombre_sommets() for _ in range(H.nombre_sommets())] # distance min
        # for i in range(H.nombre_sommets()):
        #     distance[i][i] = 0

        ## Changement du poids de tous les arcs
        for (u,v,p) in G.arcs():
            circuit_neg = 1
            cmp = 0     
            while cmp <= n and circuit_neg == 1: # circuit négatif
                w = random.randint(-10,10)
                circuit_neg = 0
                if distance[v][u] + w < 0:
                    circuit_neg = 1
                for x in H.sommets():
                    if x != u and x != v:
                        if distance[x][u] + w + distance[v][x] < 0:
                            circuit_neg = 1
                # for x in ancetres(H, u, []):
                #     # if x != u and x != v:
                #         if distance[x][u] + w + distance[v][x] < 0:
                #             circuit_neg = 1
                # for y in descendants(H, v, []):
                #     # if y != u and y != v:
                #         if distance[y][u] + w + distance[v][y] < 0:
                #             circuit_neg = 1
                cmp += 1

            # prend trop de temps --> on recommence tout (au prochain tour du while)
            if cmp > n or circuit_neg == 1: 
                graphe_ok = 0
            # sinon, il n'y a pas de pb, donc on ajoute l'arc et on met à jour les distances min
            else:
                distance[u][v] = min(distance[u][v], w)
                # print(H)
                # print("ajout arc:", u, v, w)
                # print("distance:", distance)
                H.ajouter_arc(u,v,w)

                # pred_tot = list(H.predecesseurs(u)) # pred proche (début liste) à pred éloigné (fin liste)
                # pred_i = list(H.predecesseurs(u))
                # while len(pred_i) != 0:
                #     pred_i_1 = []
                #     for x1 in pred_i: # parcours de tous les prédecesseurs actuels
                #         for x2 in H.predecesseurs(x1): # parcours de tous les prédecesseurs du prédecesseur actuel
                #             if x2 not in pred_tot: # si le prédecesseur n'est pas encore dans la liste, on l'ajoute
                #                 pred_i_1.append(x2)
                #     pred_tot += pred_i_1 # concaténation des listes de prédecesseurs
                #     pred_i = pred_i_1
                
                # while len(pred_tot) != 0:
                #     x = pred_tot.pop()
                #     if distance[x][v] > distance[x][u] + w:
                #         distance[x][v] = distance[x][u] + w

                # pred_tot = list(H.predecesseurs(u))
                # pred_i = list(H.predecesseurs(u))
                # while len(pred_i) != 0:
                #     pred_i_1 = []
                #     for x1 in pred_i: # parcours de tous les prédecesseurs actuels
                #         for x2 in H.predecesseurs(x1): # parcours de tous les prédecesseurs du prédecesseur actuel
                #             if x2 not in pred_tot: # si le prédecesseur n'est pas encore dans la liste, on l'ajoute
                #                 pred_i_1.append(x2)
                #     pred_tot += pred_i_1 # concaténation des listes de prédecesseurs
                #     pred_i = pred_i_1
                
                # succ_tot = list(H.successeurs(v)) # même principe pour les successeurs
                # succ_i = list(H.successeurs(v))
                # while len(succ_i) != 0:
                #     succ_i_1 = []
                #     for y1 in succ_i:
                #         for y2 in H.successeurs(y1):
                #             if y2 not in succ_tot:
                #                 succ_i_1.append(y2)
                #     succ_tot += succ_i_1
                #     succ_i = succ_i_1

                # changement = 1
                # while changement == 1:
                #     changement = 0
                #     for x in pred_tot: # x --> u --> v
                #         if distance[x][v] > distance[x][u] + w:
                #             distance[x][v] = distance[x][u] + w
                #             changement = 1
                #     for y in succ_tot: # u --> v --> y
                #         if distance[u][y] > w + distance[v][y]:
                #             distance[u][y] = w + distance[v][y]
                #             changement = 1
                #     for z in H.sommets():
                #         if z != u and z != v: # u --> z --> v
                #             if distance[u][v] > distance[u][z] + distance[z][v]:
                #                 distance[u][v] = distance[u][z] + distance[z][v]
                #                 changement = 1

                # changement = 1
                # while changement == 1:
                #     changement = 0
                #     for z in H.sommets():
                #         if distance[u][v] > distance[u][z] + distance[z][v]:
                #             distance[u][v] = distance[u][z] + distance[z][v]
                #             changement = 1
                #         if distance[z][v] > distance[z][u] + w:
                #             distance[z][v] = distance[z][u] + w
                #             changement = 1
                #         if distance[u][z] > w + distance[v][z]:
                #             distance[u][z] = w + distance[v][z]
                #             changement = 1

                changement = 1
                while changement == 1:
                    changement = 0
                    for z in H.sommets():
                        for y in H.sommets():
                            for x in H.sommets():
                                if distance[u][v] > distance[u][z] + distance[z][v]:
                                    distance[u][v] = distance[u][z] + distance[z][v]
                                    changement = 1
                                if distance[z][v] > distance[z][u] + w:
                                    distance[z][v] = distance[z][u] + w
                                    changement = 1
                                if distance[u][z] > w + distance[v][z]:
                                    distance[u][z] = w + distance[v][z]
                                    changement = 1
                                if x != y and y != z and x != z:
                                    if distance[x][z] > distance[x][y] + distance[y][z]:
                                        distance[x][z] = distance[x][y] + distance[y][z]
                                        changement = 1


                # pred_i = H.predecesseurs(u)
                # while len(pred_i) != 0:
                #     pred_i_1 = set()
                #     for x in pred_i:
                #         if distance[x][v] < distance[x][u] + w:
                #             distance[x][v] = distance[x][u] + w
                #             pred_i_1 |= H.predecesseurs(x)
                #     pred_i = pred_i_1
                
                # succ_i = H.successeurs(v)
                # while len(succ_i) != 0:
                #     succ_i_1 = set()
                #     for y in succ_i:
                #         if distance[u][y] > w + distance[v][y]:
                #             distance[u][y] = w + distance[v][y]
                #             succ_i_1 |= H.successeurs(y)
                #     succ_i = succ_i_1
                
                # for x in H.sommets():
                #     if x != u:
                #         distance[x][v] = min(distance[x][v], distance[x][u] + w)
                #     if x != v:
                #         distance[u][x] = min(distance[u][x], w + distance[v][x])
                # for x in ancetres(H, u, []):
                #     if x != u and x != v:
                #         distance[x][v] = min(distance[x][v], distance[x][u] + w)
                # for y in descendants(H, v, []):
                #     if y != u and y != v:
                #         distance[u][y] = min(distance[u][y], w + distance[v][y])

        ## Renvoie le graphe obtenu avec les poids de tous les arcs mis à jour sans circuit absorbant 
        if graphe_ok == 1: 
            return H
    

def union_chemin(G1, G2, G3, s):
    graphe = DictionnaireAdjacenceOrientePondere()
    graphe.ajouter_sommets(G1.sommets())
    
    chemin1, _ = BellmanFord(G1, s)
    chemin2, _ = BellmanFord(G2, s)
    chemin3, _ = BellmanFord(G3, s)
    print("chemin1 :", chemin1)
    print("chemin2 :", chemin2)
    print("chemin3 :", chemin3)
    
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
    
    
######################## MAIN ########################
    

# circuit_neg = 1
# ## TO DO : Fonction pour détecter un circuit négatif
# while circuit_neg == 1:
#     H, source = generer_graphe(5)
#     plus_court_chemin, nb_iterations = BellmanFord(H, source)

# print("H:", H)

# H, source = generer_graphe(5)
# plus_court_chemin, nb_iterations = BellmanFord(H, source)

# G1 = generer_homographe(H)
# G2 = generer_homographe(H)
# G3 = generer_homographe(H)
# print("G1:", G1)
# print("G2:", G2)
# print("G2:", G3)

# print(source)
# print(BellmanFord(H, source))
# T = union_chemin(G1, G2, G3, source)
# print(T)
# ordre_glouton = GloutonFas(T)
# print(ordre_glouton)
# print("ancien plus court chemin:", plus_court_chemin)
# print("ancien nb iter :", nb_iterations)
# print(BellmanFord2(H, source, ordre_glouton))

###########################################################

# G = DictionnaireAdjacenceOrientePondere()
# G.ajouter_sommets([0,1,2,3,4])
# G.ajouter_arcs([(0,1,0), (1,2,5), (2,3,1), (3,1,-7), (2,4,1), (3,4,-1)])
# print(G)
# print("bellman:", BellmanFord(G, 0))

#print(generer_graphe(5))
# G, s = generer_graphe(10)
# print(G)

for i in range(20):
    H, source = generer_graphe(15, 0.75)
    # print(H)
    # print("source:", source)
    print("H_bellman:", BellmanFord(H, source))

    G1 = generer_homographe(H)
    # print("G1:", G1)
    print("G1_bellman:", BellmanFord(G1, source))

    G2 = generer_homographe(H)
    # print("G2:", G2)
    print("G2_bellman:", BellmanFord(G2, source))

    G3 = generer_homographe(H)
    # print("G3:", G3)
    print("G3_bellman:", BellmanFord(G3, source))


# T = union_chemin(G1, G2, G3, source)
# print("union T:", T)

# ordre_glouton = GloutonFas(T)
# print("ordre:", ordre_glouton)

# plus_court_chemin, nb_iterations = BellmanFord(H, source)
# print("ancien plus court chemin:", plus_court_chemin)
# print("ancien nb iter :", nb_iterations)

# print("Bellman avec ordre GloutonFas:", BellmanFord2(H, source, ordre_glouton))
# print("sommets:", H.sommets())
# print("sommets:", list(H.sommets()))
# print("ordre alea :", random.shuffle(list(H.sommets())))
# ordre_alea = list(H.sommets())
# random.shuffle(ordre_alea)
# print("ordre_alea:", ordre_alea)
# print("Bellman avec ordre aléatoire:", BellmanFord2(H, source, ordre_alea))

