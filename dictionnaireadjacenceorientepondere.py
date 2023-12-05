#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implémentation d'un graphe orienté pondéré à l'aide d'un dictionnaire: les
clés sont les sommets, et les valeurs sont les successeurs du sommet donné. Les
boucles sont autorisées.

Source : Cours de L3 - Algorithmique des graphes 2022-2023 - Université
Gustave Eiffel
"""


class DictionnaireAdjacenceOrientePondere(object):
    def __init__(self):
        """Initialise un graphe sans arcs."""
        self.dictionnaire = dict()

    def ajouter_arc(self, u, v, poids):
        """Ajoute un arc du sommmet u vers le sommet v, en créant les sommets
        manquants le cas échéant."""
        # vérification de l'existence de u et v, et création(s) sinon
        if u not in self.dictionnaire:
            self.dictionnaire[u] = set()
        if v not in self.dictionnaire:
            self.dictionnaire[v] = set()
        # ajout de u (resp. v) parmi les voisins de v (resp. u) avec le poids
        self.dictionnaire[u].add((v, poids))


    def ajouter_arcs(self, iterable):
        """Ajoute tous les arcs de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple)."""
        for u, v, poids in iterable:
            self.ajouter_arc(u, v, poids)

    def ajouter_sommet(self, sommet):
        """Ajoute un sommet (de n'importe quel type hashable) au graphe."""
        self.dictionnaire[sommet] = set()

    def ajouter_sommets(self, iterable):
        """Ajoute tous les sommets de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des éléments hashables."""
        for sommet in iterable:
            self.ajouter_sommet(sommet)

    def arcs(self):
        """Renvoie l'ensemble des arcs du graphe. Un arc est représenté par un
        tuple (a, b, poids).
        """
        return {
            (u, v, poids) for u in self.dictionnaire
            for v, poids in self.dictionnaire[u]
        }

    def boucles(self):
        """Renvoie les boucles du graphe, c'est-à-dire les arcs reliant un
        sommet à lui-même."""
        retval = set()
        for u in self.dictionnaire:
            for v, poids in self.dictionnaire[u]:
                if v == u:
                    retval.add((v, poids))

        return retval

    def contient_arc(self, u, v):
        """Renvoie True si l'arc (u, v) existe, False sinon."""
        if self.contient_sommet(u) and self.contient_sommet(v):
            return v in [sommet for sommet, _ in self.dictionnaire[u]]
        return False

    def contient_sommet(self, u):
        """Renvoie True si le sommet u existe, False sinon."""
        return u in self.dictionnaire

    def degre(self, sommet):
        """Renvoie le nombre de voisins du sommet; s'il n'existe pas, provoque
        une erreur."""
        return self.degre_entrant(sommet) + self.degre_sortant(sommet)

    def degre_entrant(self, sommet):
        """Renvoie le nombre de prédécesseurs du sommet; s'il n'existe pas,
        provoque une erreur."""
        return sum(
            1 for predecesseur in self.dictionnaire
            if sommet in (v for v, _ in self.dictionnaire[predecesseur])
        )

    def degre_sortant(self, sommet):
        """Renvoie le nombre de successeurs du sommet; s'il n'existe pas,
        provoque une erreur."""
        return len(self.dictionnaire[sommet])

    def nombre_arcs(self):
        """Renvoie le nombre d'arcs du graphe."""
        return sum(len(voisins) for voisins in self.dictionnaire.values())

    def nombre_boucles(self):
        """Renvoie le nombre d'arêtes de la forme {u, u}."""
        return len(self.boucles())

    def nombre_sommets(self):
        """Renvoie le nombre de sommets du graphe."""
        return len(self.dictionnaire)

    def poids_arc(self, u, v):
        """Renvoie le poids de l'arc entre u et v, None s'il n'existe pas."""
        for voisin, poids in self.dictionnaire[u]:
            if voisin == v:
                return poids

    def predecesseurs(self, sommet):
        """Renvoie les prédécesseurs du sommet; s'il n'existe pas, provoque une
        erreur."""
        return {
            predecesseur for predecesseur in self.dictionnaire
            if sommet in (v for v, _ in self.dictionnaire[predecesseur])
        }

    def retirer_arc(self, u, v):
        """Retire l'arc (u, v) s'il existe; provoque une erreur sinon."""
        self.dictionnaire[u].remove(v)  # plante si u ou v n'existe pas
        # trouver le poids de l'arc (u, v) s'il existe pour pouvoir le retirer
        for voisin, p in self.dictionnaire[u]:
            if voisin == v:
                self.dictionnaire[u].remove((v, p))  # plante si v n'existe pas
                break

    def retirer_arcs(self, iterable):
        """Retire tous les arcs de l'itérable donné du graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple)."""
        for u, v in iterable:
            self.retirer_arc(u, v)

    def retirer_sommet(self, sommet):
        """Efface le sommet du graphe, et retire tous les arcs qui lui
        sont incidents."""
        # retrait du sommet et de ses successeurs
        del self.dictionnaire[sommet]
        # retrait des arcs issus de ses prédécesseurs
        for u in self.dictionnaire:
            self.dictionnaire[u].discard(sommet)

    def retirer_sommets(self, iterable):
        """Efface les sommets de l'itérable donné du graphe, et retire toutes
        les arêtes incidentes à ces sommets."""
        for sommet in iterable:
            self.retirer_sommet(sommet)

    def sommets(self):
        """Renvoie l'ensemble des sommets du graphe."""
        return set(self.dictionnaire.keys())

    def sous_graphe_induit(self, iterable):
        """Renvoie le sous-graphe induit par l'itérable de sommets donné."""
        G = DictionnaireAdjacenceOriente()
        G.ajouter_sommets(iterable)
        for u, v, poids in self.arcs():
            if G.contient_sommet(u) and G.contient_sommet(v):
                G.ajouter_arc(u, v, poids)
        return G

    def successeurs(self, sommet):
        """Renvoie les successeurs du sommet; s'il n'existe pas, provoque une
        erreur."""
        return {v for v, _ in self.dictionnaire[sommet]}

    def voisins(self, sommet):
        """Renvoie l'ensemble des voisins du sommet donné."""
        return self.successeurs(sommet).union(self.predecesseurs(sommet))

    def __str__(self):
        """Formatage simple"""
        res = ["Graphe orienté avec %d sommets : %s" 
        % (len(self.dictionnaire), str(list(self.sommets())))]
        for k,v in self.dictionnaire.items():
            for y, poids in v:
                res.append("%s -[%d]-> %s" % (k, poids, y))
        return "\n".join(res)

    def __repr__(self):
        return self.__str__()


    def saveGraph(self, file, source):
        file.write("{} {}".format(self.nombre_sommets(), source))
        file.write('\n')
        for v in self.sommets(): 
            lst_u = self.predecesseurs(v)
            for u in lst_u:
                p = self.poids_arc(u, v)
                file.write('{} {} {}'.format(u,v,p))
                file.write('\n')

    def grapheFromFile(file):
        texts = file.readlines()
        g = DictionnaireAdjacenceOrientePondere()
        n, s = texts[0].split(' ')
        g.ajouter_sommets([i for i in range(int(n))])
        texts.pop(0)
        for text in texts:
            u, v, p = text.split(' ')
            g.ajouter_arc(int(u), int(v), int(p))

        return g, int(s)
    


def main():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    main()
