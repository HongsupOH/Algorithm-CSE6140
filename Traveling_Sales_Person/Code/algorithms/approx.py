import time
import random
import networkx as nx
import numpy as np
from heapq import *

class Approx:
    def __init__(self, graph, timelimit, seed, source=-1):
        print(graph.city)
        random.seed(int(seed))
        np.random.seed(int(seed))
        self.G = graph.G
        self.nxG = graph.nxG
        self.N = len(graph.G)
        self.start = time.time()
        self.trace = ""
        T = nx.minimum_spanning_tree(self.nxG)
        odds = []
        for i in range(self.N):
            if T.degree(i)%2==1:
                odds.append(i)
        odds_graph = nx.Graph()
        for i in odds:
            for j in odds:
                if i<j:
                    odds_graph.add_edge(i,j,weight=10**8-self.G[i][j])
        matching = nx.algorithms.matching.max_weight_matching(odds_graph)
        M = nx.MultiGraph(T)
        for i,j in matching:
            M.add_edge(i,j,weight=self.G[i][j])
        self.M = M
        self.min_tour = self.Search(source)

    def Search(self, source):
        min_tour = {"tour": [], "weight": 10**9}
        if source != -1:
            ec = nx.algorithms.euler.eulerian_circuit(self.M, source=source)
            p = []
            for e in ec:
                if e[0] not in p:
                    p.append(e[0])
            w = self.get_tour_weight(p)
            min_tour = {"tour": p, "weight": w}
            return min_tour
        else:
            tours = []
            hs = set()
            for i in range(self.N):
                ec = nx.algorithms.euler.eulerian_circuit(self.M, source=i)
                p = []
                for e in ec:
                    if e[0] not in p:
                        p.append(e[0])
                w = self.get_tour_weight(p)
                z_idx = p.index(0)
                p = p[z_idx:] + p[:z_idx]
                h = hash(str(p+[w]))
                if h not in hs:
                    tours.append({'weight':w, 'tour':p})
                    hs.add(h)
                if min_tour['weight'] > w:
                    min_tour = {"tour": p, "weight": w}
                    self.trace += "{1:4f} {0}\n".format(w,time.time()-self.start)
            print(min_tour)
            self.all_tours = sorted(tours, key=lambda k: k['weight'])
            return min_tour

    def get_results(self):
        sol = self.get_min_tour_printable()
        return sol, self.trace, self.min_tour

    def get_min_tour_printable(self):
        tour = self.min_tour['tour']
        if len(tour) == 0:
            return "Something Wrong"
        s = "{0}\n".format(self.get_tour_weight(tour))
        for i in range(len(tour)-1):
            r = tour[i], tour[i+1], self.G[tour[i]][tour[i+1]]
            s += "{0} {1} {2}\n".format(r[0], r[1], r[2])
        r = tour[-1], tour[0], self.G[tour[0]][tour[-1]]
        s += "{0} {1} {2}\n".format(r[0], r[1], r[2])
        return s

    def get_tour_weight(self, tour):
        '''
        Return the weight of this current tour
        '''
        d = 0
        if len(tour) == 1:
            return d
        for i in range(len(tour)-1):
            d += self.G[tour[i]][tour[i+1]]
        return d+self.G[tour[0]][tour[-1]]
