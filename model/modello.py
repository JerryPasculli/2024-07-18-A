import copy
import math

import networkx as nx

from database.DAO import DAO
from model.arco import Arco


class Model:
    def __init__(self):
        self._G = nx.DiGraph()
        self._nodi = []
        self._Dnodi = {}
        self._archi = []
        self._lunghezza = 0
        self._peso = math.inf
        self._percorso = []


    def creaArco(self, v1, v2):
        self._G = nx.DiGraph()
        self._nodi = DAO.getNodi(v1, v2)
        self._Dnodi = {}
        self._archi = []
        self._G.add_nodes_from(self._nodi)
        for element in self._nodi:
            stringa = element.GeneID + "-" + element.Function
            self._Dnodi[stringa] = element
        lista = DAO.getArchi(v1, v2)
        for element in lista:
            e1 = element[0] + "-" + element[1]
            e2 = element[2] + "-" + element[3]
            nodo1 = self._Dnodi[e1]
            nodo2 = self._Dnodi[e2]
            arco = Arco(nodo1, nodo2, element[4])
            nodo1.aggiungiArco()
            self._archi.append(arco)
            self._G.add_edge(nodo1, nodo2, weight=element[4])
        stringa = (f"Grafo creato con {self._G.number_of_nodes()} nodi e {self._G.number_of_edges()} archi\n\nI cinque nodi col maggior"
                   f"numero di archi uscenti sono:")
        self._nodi.sort(reverse=True)
        for i in range(5):
            lui = self._nodi[i]
            tot = 0
            for element in self._G.neighbors(lui):
                tot = self._G[lui][element]["weight"] + tot
            stringa = stringa + "\n" + lui.__str__() + f"| peso.tot: {tot}"
        return stringa

    def cromos(self):
        lista = DAO.get_all_genes()
        return lista


    def percorso(self):
        self._lunghezza = 0
        self._peso = math.inf
        self._percorso = []
        for element in self._nodi:
            parziale = [element]
            self.itera(parziale, element, 0, -math.inf)
        stringa = f"Cammino con valore lunghezza massima:{self._lunghezza} e peso: {self._peso}"
        for element in self._percorso:
            stringa = stringa + f"\n{element.__str__()}"
        return stringa

    def itera(self, parziale, ultimo, peso, ultimoArco):
        if len(parziale)>self._lunghezza:
            self._percorso = copy.deepcopy(parziale)
            self._lunghezza = len(parziale)
            self._peso = peso
        if len(parziale) == self._lunghezza:
            if peso<self._peso:
                self._percorso = copy.deepcopy(parziale)
                self._lunghezza = len(parziale)
                self._peso = peso
        for element in self._G.neighbors(ultimo):
            if element not in parziale:
                if element.Essential != ultimo.Essential:
                    if self._G[ultimo][element]["weight"]>=ultimoArco:
                        peso1 = peso + self._G[ultimo][element]["weight"]
                        parziale.append(element)
                        self.itera(parziale, element, peso1, self._G[ultimo][element]["weight"])
                        parziale.pop()




