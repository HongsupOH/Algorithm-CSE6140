#MST Approximation code
import numpy as np
import math
import sys
import timeit as tt


class MST_App:
    def __init__(self, graph, seed=5, cutoff=600):
        temp = graph.split('.')
        self.city = temp[0]
        self.rand_seed = seed
        self.cutoff_time = cutoff
        self.path = []
        self.total = 0

    def read_tsp(self):
        L = []
        with open('./DATA/'+self.city+'.tsp') as f:
            for line in f:
                if line == 'EOF\n':
                    break
                l = line[:-1].split(' ')
                try:
                    if len(l) > 2:
                        x_c = float(l[1])
                        y_c = float(l[2])
                        L.append({'x': x_c, 'y': y_c})
                except ValueError:
                    pass

            N = len(L)
            G = [[0 for i in range(N)] for j in range(N)]
            for i in range(N):
                for j in range(N):
                    if i == j:
                        G[i][j] = float('inf')
                    else:
                        G[i][j] = int(
                            round(math.sqrt((L[i]['x'] - L[j]['x']) ** 2 + (L[i]['y'] - L[j]['y']) ** 2)))
        return G

    def MST(self, G):
        GG = np.array(G)
        E = []
        visited = [0]
        while len(visited) < len(G):
            (row, col) = np.unravel_index(
                GG[visited].argmin(), GG[visited].shape)
            visited.append(col)

            E.append((visited[row], col))

            s = [(col, v) for v in visited]

            for (k, v) in s:
                GG[k][v] = float('inf')
                GG[v][k] = float('inf')

        #duplicate mst
        E_e = [(y, x) for (x, y) in E]
        E.extend(E_e)

        return E

    def p_order(self, E, parent):
        if parent not in self.path:
            self.path.append(parent)
            child = [x[1] for x in E if x[0] == parent]
            if len(child) > 0:
                for node in child:
                    self.p_order(E, node)
            else:
                return

    def road(self, G):
        R = []
        for i in range(len(self.path)-1):
            dist = G[self.path[i]][self.path[i+1]]
            R.append((self.path[i], self.path[i+1], dist))
            self.total += dist
        dist = G[self.path[-1]][self.path[0]]
        R.append((self.path[-1], self.path[0], dist))
        self.total += dist
        return R

    def write_data(self, output, total):
        total = str(total)
        with open('output/'+self.city + "_MSTApprox_" + str(self.rand_seed)+'.out', 'w') as f:
            f.write(total)
            f.write('\n')
            for (a, b, c) in output:
                f.write(str(a) + ' ' + str(b) + ' ' + str(int(c)))
                f.write('\n')

    def write_trace(self, time, total):
        with open('output/'+self.city + "_MSTApprox_" + str(self.rand_seed)+'.trace', 'w') as f:
            f.write('{:.2f} {}\n'.format(time, total))

    def generate_tour(self):
        start = tt.default_timer()
        self.total = 0.0
        self.path = []
        graph = self.read_tsp()
        edge = self.MST(graph)
        self.p_order(edge, self.rand_seed)
        output = self.road(graph)
        stop = tt.default_timer()
        self.write_trace(stop-start, int(self.total))
        self.write_data(output, self.total)

    def get_results(self):
        return self.path
