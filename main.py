
from part2.BinPacking import BinPacking
from part2.Graphe import Graphe

if __name__ == '__main__':
    g=Graphe()
    g.chargerFichier("DSJC1000.5.txt")
    print("bestFitDecreasingPacking ", g.binPacking.bestFitDecreasingPacking().__len__())
    print("firstFitDecreasingPacking ", g.binPacking.firstFitDecreasingPacking().__len__())
    print("fractionalPacking ", g.binPacking.fractionalPacking())
    nbBoite,remplissage=g.dsaturWithBFDpacking()
    print(" dsaturWithBFDpacking",nbBoite)
    nbBoite, remplissage= g.dsaturWithFFDpacking()
    print(" dsaturWithFFDpacking",nbBoite)