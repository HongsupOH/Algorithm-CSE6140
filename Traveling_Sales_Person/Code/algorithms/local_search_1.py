import time
import random
'''
Implementation of our 2 opt algorithm.
1.  Chose random route. Route must start and end with same node. There shouldn't be other duplicate nodes. 
2.  swap two edges in a way that crossed edges gets removed (locally. This action may cause other crossings globally.). 
3.  Repeat 2-opt swap till there is no improvement in total cost. When there is no improvement that is local optimum 
4.  goto step 1 (this is a restart)
5.  Exit when time up and chose the best out of all found local optimums. 
'''


class LocalSearch1:
    def __init__(self, graph, timelimit, seed):
        self.graph = graph
        self.G = graph.G
        self.N = len(graph.G)
        self.start = time.time()
        self.trace = ""
        self.timelimit = timelimit
        random.seed(seed)
        self.Search()
        print(self.min_tour)

    def get_results(self):
        sol = self.get_min_tour_printable()
        # print(sol)
        # print(self.trace)
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
        improved = True  # Assume current best is not a best solution
        while improved:
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
                    if new_cost < self.cost(best):
                        #if new best is so far best, update the trace log.
                        if new_cost < self.min_tour['weight']:
                            self.trace += "{1:4f} {0}\n".format(
                                new_cost, time.time() - self.start)
                            self.min_tour = {
                                "tour": new_route[:-1],
                                "weight": new_cost
                            }
                        best = new_route
                        # look if there can be more improvement.
                        improved = True
                if self.isTimeup():
                    break
            route = best
        return best

    def Search(self):
        #Random initial solution
        s = random.sample(range(self.N), self.N)
        s.append(s[0])
        # so far global min
        self.min_tour = {"tour": s, "weight": self.cost(s)}
        i = 0
        while not self.isTimeup() and i < self.N**4:
            self.two_opt(s)
            # Restart two_opt with new random solution.
            s = random.sample(s[0:self.N], self.N)
            s.append(s[0])
            i+=1

    def get_min_tour_printable(self):
        tour = self.min_tour['tour']
        if len(tour) == 0:
            return "Something Wrong"
        s = "{0}\n".format(self.min_tour['weight'])
        for i in range(len(tour)-1):
            r = tour[i], tour[i+1], self.G[tour[i]][tour[i+1]]
            s += "{0} {1} {2}\n".format(r[0], r[1], r[2])
        r = tour[-1], tour[0], self.G[tour[0]][tour[-1]]
        s += "{0} {1} {2}\n".format(r[0], r[1], r[2])
        return s
