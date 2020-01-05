import collections
from builtins import range

from part2.BinPacking import BinPacking
import random

class Graphe:
    def __init__(self, N=1,tailles=[],HAUTEUR=150):
        self.edges = [set([]) for _ in range(N)]
        self.N = N
        self.sommetsTaille=tailles
        self.binPacking=BinPacking({sommet:hauteur for sommet,hauteur in enumerate(tailles) },self)
        self.HAUTEUR=HAUTEUR
    def chargerFichier(self,name):
        with open(name,"r") as file:
            line = file.readline()
            while line.startswith("c"):
                line=file.readline()
            self.N=int(line.split(" ")[2])+1
            self.edges = [set([]) for _ in range(self.N)]
            self.sommetsTaille={x:random.randrange(10,50) for x in range(self.N)}
            self.binPacking=BinPacking(self.sommetsTaille,self,150)
            line = file.readline()
            while line and line.startswith("e"):
                edge=line.split(" ")
                self.ajouterVoisin(int(edge[1]),noeud=int(edge[2]))
                line = file.readline()
            satur = self.dSatur()
            sommets, couleurs = zip(*satur)
            self.sommetGroupByCouleur = {c: [] for c in set(couleurs)}
            for obj, col in satur:
                self.sommetGroupByCouleur[col].append(obj)

    def voisin(self, noeud):
        return self.edges[noeud]
    def ajouterVoisin(self, *voisin, noeud):
        for v in voisin:
            self.edges[noeud].add(v)
            self.edges[v].add(noeud)
    def getSommets(self):
        return [i for i in range(self.N)]
    def dSatur(self):
        #trier les noeuds par ordre dec
        sommetDegre = sorted([(i, len(self.voisin(i))) for i in range(self.N)], key=lambda x: x[1], reverse=True)
        sommets, _ = zip(*sommetDegre)
        U = list(sommets)
        del U[len(sommets) - 1]#supprimer le sommet  0.
        #initialisation
        noeudCouleur = {U[0]: 1}
        C = [U[0]]
        del U[0]
        while len(U):
            maxiSatur = -1
            noeudSuiv = None
            couleurVoisin=set([])
            for u in U:
                satur=set([])
                for s in self.voisin(u):
                    if s in noeudCouleur.keys():
                        satur.add(noeudCouleur[s])
                if len(satur) > maxiSatur:
                    maxiSatur = len(satur)
                    noeudSuiv = u
                    couleurVoisin = satur
                elif len(satur) == maxiSatur:
                    if len(self.voisin(noeudSuiv)) < len(self.voisin(u)):
                        noeudSuiv = u
                        couleurVoisin = satur
            i=1
            while  i<=max(couleurVoisin)+1 and i in couleurVoisin:
                i+=1
            noeudCouleur[noeudSuiv]=i
            U.remove(noeudSuiv)
            C.append(noeudSuiv)
        return list(noeudCouleur.items())
    def dsaturWithFFDpacking(self):
        size=0
        result=[]
        for sommeDeMemeCouleurs in self.sommetGroupByCouleur.values():
            b = BinPacking({sommet:self.sommetsTaille[sommet] for sommet in sommeDeMemeCouleurs}, tailleBoite=self.HAUTEUR)
            res=b.firstFitDecreasingPacking()
            size+=len(res)
            result+=res
        return size,result

    def dsaturWithBFDpacking(self):
        size=0
        resultat=[]
        for objetMemeCouleurs in self.sommetGroupByCouleur.values():
           # b = BinPacking({sommet: random.randrange(10, 50) for sommet in objetMemeCouleurs}, grapheConflit=self,tailleBoite=tailleBoite)
            b = BinPacking({sommet: self.sommetsTaille[sommet] for sommet in objetMemeCouleurs},tailleBoite=self.HAUTEUR,)
            res = b.bestFitDecreasingPacking()
            resultat+=res
            size += len(res)
        return size,resultat


