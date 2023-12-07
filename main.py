from dictionnaireadjacenceorientepondere import DictionnaireAdjacenceOrientePondere
from bellmanFord import BellmanFord, BellmanFord2, GloutonFas, BellmanFordAleatoireUniforme
from genererGraphe import union_chemin, generer_homographe, union_chemin_iter

file = open('graphe.txt', 'r')
graphe, source= DictionnaireAdjacenceOrientePondere.grapheFromFile(file)
file.close()

file = open('graphe1.txt', 'r')
g1, _= DictionnaireAdjacenceOrientePondere.grapheFromFile(file)
file.close()

file = open('graphe2.txt', 'r')
g2, _= DictionnaireAdjacenceOrientePondere.grapheFromFile(file)
file.close()

file = open('graphe3.txt', 'r')
g3, _= DictionnaireAdjacenceOrientePondere.grapheFromFile(file)
file.close()

while True:
        G4 = generer_homographe(graphe)
        parent, k, isNegatif = BellmanFord(G4, source)
        if isNegatif == 0:
            break


while True:
        G5 = generer_homographe(graphe)
        parent, k, isNegatif = BellmanFord(G5, source)
        if isNegatif == 0:
            break


while True:
        G6 = generer_homographe(graphe)
        parent, k, isNegatif = BellmanFord(G6, source)
        if isNegatif == 0:
            break

# T = union_chemin(g1, g2, g3, source)
 T= union_chemin_iter([g1,g2,g3,G4,G5,G6], source)

ordre = GloutonFas(T)
print('ordre : ', ordre)

parent, k, _ = BellmanFordAleatoireUniforme(graphe, source)
print('ancienne exécution, resultat: {}, nb itération: {}'.format(parent, k))

parent, k, _ = BellmanFord2(graphe, source, ordre)
print('nouvelle exécution, resultat: {}, nb itération: {}'.format(parent, k))
