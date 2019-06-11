import time
import random
import math
from itertools import permutations
from random import choice

'''
Implement SA for our second local seach algorithm. 
'''

class LocalSearch2:
    def __init__(self, graph, timelimit, seed):
        self.graph = graph
        self.G = graph.G
        self.N = len(graph.G)
        self.start = time.time()
        self.trace = ""
        self.timelimit = timelimit
        self.min_tour = {"tour": [], "weight": float('Inf')}
        random.seed(seed)
        self.Search()

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

    def get_results(self):
        sol = self.get_min_tour_printable()
        # print(sol)
        # print(self.trace)
        return sol, self.trace, self.min_tour

    def isTimeup(self):
        return (time.time() - self.start) >= self.timelimit
    
    # def cost(self, s):
    #     total = 0
    #     for ind in range(1, len(s)):
    #         total += self.G[s[ind-1]][s[ind]]
    #     return total
    def tabu_same(self,items):
        return all(x == items[0] for x in items)
    
    def Search(self):
        # parameters for SA
        temperature = len(self.G) * 200
        end_temperature = 10
        cooling_rate = 0.95
        max_num_reheat = 5
        max_iter_per_temp = 6000
        curt_num_reheat = 0
        best_temp = temperature

        # Random initial solution
        current_route = random.sample(range(self.N), self.N)
        # make a circle for the curt_route
        # current_route.append(current_route[0])
        while curt_num_reheat < max_num_reheat:
            if self.isTimeup():
                break 
            while temperature > end_temperature:
                if self.isTimeup():
                    break
                curt_iter_this_temp = 0
                while curt_iter_this_temp < max_iter_per_temp:
                    # print(curt_iter_this_temp)
                    if self.isTimeup():
                        break
                    # 2-opt to generate next new route
                    # [i,j] = sorted(random.sample(range(len(self.G)),2))
                    # next_route =  current_route[:i] + current_route[j:j+1] +  current_route[i+1:j] + current_route[i:i+1] + current_route[j+1:]
                    
                    # 3-opt to generate next new route
                    a = random.randint(0, len(current_route) - 2)
                    b = random.randint(a+1, len(current_route) - 1)
                    c = random.randint(b+1, len(current_route))
                    # a, b, c = choice(list( permutations( (a, b, c) ) ) )
                    next_route = current_route[:a] + current_route[a:b][::-1] + current_route[b:c][::-1] + current_route[c:]
                    # print(current_route)
                    # print(next_route)
                    next_cost = self.get_tour_weight(next_route)
                    current_cost = self.get_tour_weight(current_route)
                    diff = next_cost - current_cost
                    if diff < 0:
                        current_route = next_route
                        current_cost = next_cost
                    else:
                        if math.exp(-diff/temperature) > random.random():
                            current_route = next_route
                            current_cost = next_cost
                    if current_cost < self.min_tour["weight"]:
                        # print(current_cost)
                        self.trace += "{1:4f} {0}\n".format(current_cost, time.time() - self.start)
                        self.min_tour = {
                            "tour": current_route,
                            "weight": current_cost
                        }
                        curt_num_reheat = 0
                        best_temp = temperature
                    curt_iter_this_temp += 1
                temperature = temperature * cooling_rate
            curt_num_reheat += 1
            temperature = best_temp * 100
            # print("reheat start!")
            # print(temperature)
            current_route = self.min_tour["tour"]
        

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
