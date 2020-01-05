from  collections import OrderedDict
import math
class BinPacking():
    """docstring fo BinPacking.
    """
    def __init__(self,sommetsTailles,grapheConflit=None,tailleBoite=150):
        self.HAUTEUR=tailleBoite
        self.sommetsTailles=dict(sommetsTailles)
        self.graphe=grapheConflit
    def fractionalPacking(self):
        return  math.ceil(sum(list(self.sommetsTailles.values())) / self.HAUTEUR)

    def firstFitDecreasingPacking(self):
        sommetsOrdre=sorted([s for s in self.sommetsTailles],key=lambda s:self.sommetsTailles[s],reverse=True)#les sommets dans l'ordre dec
        result = [[]]
        somme = 0
        dejachoisi = []

        for i in sommetsOrdre:
            estAjouter=False
            for j in range(len(result)):
                _,hauteurs=(0,[0]) if len(result[j])==0 else zip(*result[j])
                somme=sum(list(hauteurs))+self.sommetsTailles[i]
                if not i in dejachoisi and not self.hasConflict(i, j, result) and somme<=self.HAUTEUR:
                    result[j].append((i,self.sommetsTailles[i]))
                    estAjouter=True
                    break
            if not estAjouter:
                result.append([(i,self.sommetsTailles[i])])
        return result
    def bestFitDecreasingPacking(self):
        sommetsOrdonne = sorted([s for s in self.sommetsTailles], key=lambda s: self.sommetsTailles[s], reverse=True)
        result = [[(sommetsOrdonne[0],self.sommetsTailles[sommetsOrdonne[0]])]]
        dejachoisi = [sommetsOrdonne[0]]
        while len(dejachoisi)!=len(sommetsOrdonne):
            for sommet in sommetsOrdonne:
                if not sommet in dejachoisi:
                    c = []
                    for j in range(len(result)):
                        _,h=zip(*result[j])#result[[(indice,objet),(....)]...]
                        c.append(sum(h)+self.sommetsTailles[sommet])#ajouter lobjet dans toutes les boites
                    minBox = self.HAUTEUR
                    indexBox = -1
                    for i,somme in enumerate(c):
                        if somme <=minBox   and not self.hasConflict(sommet, i,result):  # trouver la boite de contenu minimale et qui  ne depasse pas passe la taille des boites
                            minBox = somme
                            indexBox = i
                    if indexBox == -1:
                        indexBox=len(result)
                        result.append([])
                    result[indexBox].append((sommet, self.sommetsTailles[sommet]))
                    dejachoisi.append(sommet)
        return result
    def hasConflict(self,sommet,numeroBox,result):
        #result[(sommet,taille)...]
        box=None
        if result[numeroBox]!=None and len(result[numeroBox])!=0:
            box,_=zip(*result[numeroBox])
        if self.graphe==None or box==None:
            return False
        else:
            for o in box:
                if sommet in self.graphe.voisin(o):
                    return True
            return False
    def getMinimalBox(self,result,sommet):
        if len(result)==0 or len(result[0])==0:
            return 0
        # format result[[(sommet,Hauteur)...],[...]]
        c=[result[i].copy() for i in range(len(result))]#copier toutes les boites et leurs contenus
        size=len(c)
        for i in range(size):
                c[i].append((sommet,self.sommetsTailles[sommet])) #Ajouter lobjet dans toutes les boites
        minBox=sum(self.sommetsTailles.values())
        indexBox=-1
        for i in range(len(c)):
            _,hauteurs=zip(*c[i])
            somme=sum(hauteurs)#contenu total de chaque boite
            if somme<minBox and somme<=self.HAUTEUR and  not self.hasConflict(sommet, i, result):#trouver la boite de contenu minimale et qui  ne depasse pas passe la taille des boites
                minBox=somme
                indexBox=i
        if indexBox==-1:
            return len(result)
        return indexBox #retourner l'indice de la boite minimale


