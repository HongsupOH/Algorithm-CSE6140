import math
from copy import deepcopy
import networkx as nx
import numpy as np
import sys
inf = 10**10

class Graph:
    def __init__(self, filename):
        self.filename = filename
        self.load_from_file()

    def parse_GEO(self, node):
        i, x, y = node
        i = int(i)
        PI = 3.141592
        deg = int(x)
        min = x - deg
        lat = PI*(deg + 5.0*min/3.0)/180.0
        deg = int(y)
        min = y - deg
        lon = PI*(deg + 5.0*min/3.0)/180.0
        return i, lat, lon

    def get_GEO_distance(self, node1, node2):
        i, lat_i, lon_i = node1
        j, lat_j, lon_j = node2
        i, j = int(i)-1, int(j)-1
        R = 6378.388
        q1 = math.cos(lon_i-lon_j)
        q2 = math.cos(lat_i-lat_j)
        q3 = math.cos(lat_i+lat_j)
        d = int(R * math.acos(0.5*((1.0+q1)*q2 - (1.0-q1)*q3)) + 1.0)
        return i, j, d

    def get_EUV_2D_distance(self, node1, node2):
        i, x_i, y_i = node1
        j, x_j, y_j = node2
        i, j = int(i)-1, int(j)-1
        xd = x_i-x_j
        yd = y_i-y_j
        d = math.sqrt((xd*xd+yd*yd))
        return i, j, int(d+0.5)

    def load_from_file(self):
        nodes_list = []
        params = {}
        with open(self.filename, "r") as f:
            line = f.readline()
            while ':' in line:
                key, value = line.split(':')
                params[key] = value.strip()
                line = f.readline()
            line = f.readline()
            while 'EOF' not in line:
                n, x, y = line.strip().split(' ')
                n, x, y = n.strip(), x.strip(), y.strip()
                n, x, y = float(n), float(x), float(y)
                if params['EDGE_WEIGHT_TYPE'] == 'GEO':
                    n, x, y = self.parse_GEO((n, x, y))
                nodes_list.append([n, x, y])
                line = f.readline()

        dim = int(params['DIMENSION'])
        graph = [[0 for i in range(dim)] for j in range(dim)]

        self.city = params['NAME']

        if params['EDGE_WEIGHT_TYPE'] == 'EUC_2D':
            dist_func = self.get_EUV_2D_distance
        else:
            dist_func = self.get_GEO_distance

        for node1 in nodes_list:
            for node2 in nodes_list:
                i, j, distance = dist_func(node1, node2)
                if i == j:
                    distance = inf
                graph[i][j] = distance
                graph[j][i] = distance

        graph = np.array(graph)
        self.nxG = nx.from_numpy_matrix(graph)
        for i in range(len(nodes_list)):
            self.nxG.remove_edge(i,i)
        self.G = graph

    def copy(self):
        return deepcopy(self.G)

    def __repr__(self):
        return repr(self.G)