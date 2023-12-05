from dictionnaireadjacenceorientepondere import DictionnaireAdjacenceOrientePondere
from bellmanFord import BellmanFord, BellmanFord2, GloutonFas, BellmanFordAleatoireUniforme
from genererGraphe import union_chemin

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

T = union_chemin(g1, g2, g3, source)


ordre = GloutonFas(T)
print('ordre : ', ordre)

parent, k, _ = BellmanFordAleatoireUniforme(graphe, source)
print('ancienne exécution, resultat: {}, nb itération: {}'.format(parent, k))

parent, k, _ = BellmanFord2(graphe, source, ordre)
print('nouvelle exécution, resultat: {}, nb itération: {}'.format(parent, k))
