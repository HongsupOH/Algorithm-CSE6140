import time
import random
from algorithms.approx import Approx
import sys
inf = 10**9


class BranchAndBound:
    '''
    https://people.eecs.berkeley.edu/~demmel/cs267/assignment4.html
    '''

    def __init__(self, graph, timelimit, seed):
        self.timelimit = timelimit
        self.G = graph.G
        self.nxG = graph.nxG
        self.N = len(graph.G)
        self.start = time.time()
        self.trace = ""
        random.seed(seed)
        self.Search()
        print(self.min_tour)

    def Search(self):
        F = [(1, [0])]
        B = 10**9, [0]
        while len(F) > 0:
            if time.time()-self.start > self.timelimit:
                break
            best_config, F = self.choose(F)
            options = self.expand(best_config[1])
            for path in options:
                w = self.get_tour_weight(path)
                # print(w, len(path), B[0], self.N)
                if len(path) == self.N:
                    # print(w, B[0])
                    if w < B[0]:
                        # print(w,B[0])
                        self.trace += "{1:4f} {0}\n".format(
                            w, time.time()-self.start)
                        B = (w, path)
                if time.time()-self.start > self.timelimit:
                    break
                if not self.prune((w, path), B, best_config):
                    F.append((len(path), path))
        self.min_tour = {"tour": B[1], "weight": B[0]}

    def choose(self, F):
        best = max(F)
        F.remove(best)
        return best, F

    def expand(self, path):
        options = []
        all_v = set(list(range(self.N)))
        ind = list(all_v-set(path))
        for i in ind:
            np = path+[i]
            options.append(np)
        return options

    def prune(self, curr, best, prev):
        if best[0] < curr[0]:
            return True
        current_lb = self.get_lower_bound(curr[1]) + curr[0]
        if best[0] < current_lb:
            return True
        return False

    def get_results(self):
        sol = self.get_min_tour_printable()
        return sol, self.trace, self.min_tour

    def get_lower_bound(self, path):
        '''
        Lower bound of the remaining graph that excludes 
        vertices already in path
        This uses min 2 edge from every vertex
        '''
        w = 0
        all_v = set(list(range(self.N)))
        ind = list(all_v-set(path))
        # We need to exclude vertices already in path
        for i in ind:
            min1 = min2 = inf
            for j in ind:
                if i == j:
                    continue
                if min1 > self.G[i][j]:
                    min2, min1 = min1, self.G[i][j]

            if min2 != inf:
                w += min1+min2
            elif min1 != inf:
                w += min1

        return int(w/2)

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

    def get_min_tour_printable(self):
        tour = self.min_tour['tour']
        if len(tour) == 0:
            return "Something Wrong, try again"
        s = "{0}\n".format(self.min_tour['weight'])
        for i in range(len(tour)-1):
            r = tour[i], tour[i+1], self.G[tour[i]][tour[i+1]]
            s += "{0} {1} {2}\n".format(r[0], r[1], r[2])
        r = tour[-1], tour[0], self.G[tour[0]][tour[-1]]
        s += "{0} {1} {2}\n".format(r[0], r[1], r[2])
        return s
