import time
import random
from algorithms import Approx
import heapq


class Hybrid1:
    def __init__(self, graph, timelimit, seed):
        self.graph = graph
        self.G = graph.G
        self.N = len(graph.G)
        self.start = time.time()
        self.trace = ""
        self.timelimit = timelimit
        random.seed(seed)
        self.seed = seed
        self.Search()
        print(self.min_tour)

    def get_results(self):
        sol = self.get_min_tour_printable()
        return sol, self.trace, self.min_tour

    def cost(self, s):
        total = 0
        for ind in range(1, len(s)):
            total += self.G[s[ind-1]][s[ind]]
        return total

    def isTimeup(self):
        return (time.time() - self.start) >= self.timelimit

    def two_opt(self, route):
        best = route
        best_cost = self.cost(route)
        improved = True  # Assume current best is not a best solution
        c = 0
        while improved:
            h = hash(str(route))
            if h in self.tabu:
                # print("Tabu")
                break
            self.tabu.add(h)
            improved = False
            for i in range(1, len(route) - 2):
                for j in range(i + 2, len(route)):
                    if self.isTimeup():
                        improved = False  # time up. No need to check for improvement
                        break
                    new_route = route[:]
                    # this is the 2woptSwap
                    new_route[i:j] = route[j - 1:i - 1:-1]
                    new_cost = self.cost(new_route)
                    if new_cost < best_cost:
                        #if new best is so far best, update the trace log.
                        if new_cost < self.min_tour['weight']:
                            self.trace += "{1:4f} {0}\n".format(
                                new_cost, time.time() - self.start)
                            # print("{1:4f} {0}\n".format(
                            #     new_cost, time.time() - self.start))
                            self.min_tour = {
                                "tour": new_route[:-1],
                                "weight": new_cost
                            }
                        best = new_route
                        best_cost = new_cost
                        # look if there can be more improvement.
                        improved = True
                if self.isTimeup():
                    break
            route = best
        return best

    def Search(self):
        # so far global min
        self.min_tour = {"tour": [], "weight": 10**9}
        self.tabu = set()
        approx = Approx(self.graph, self.timelimit, self.seed)
        possible_tours = approx.all_tours
        for i in random.sample(range(len(possible_tours)), len(possible_tours)):
            t = approx.all_tours[i]
            w = t['weight']
            path = t['tour']
            # print('Input', i, w, path)
            path.append(path[0])
            self.two_opt(path)
            # print('output', self.min_tour)
            # print('-'*50)
            if self.isTimeup():
                break

    def get_min_tour_printable(self):
        tour = self.min_tour['tour']
        if len(tour) == 0:
            return "Something Wrong"
        s = "{0}\n".format(self.min_tour['weight'])
        for i in range(len(tour)-1):
            r = tour[i], tour[i+1], self.G[tour[i]][tour[i+1]]
            s += "{0} {1} {2}\n".format(r[0], r[1], r[2])
        return s
