##
# hcc.py
# <your name here>
# Georgia Institute of Technology, Fall 2018
#
# Compute HC centrality measure
def compute(g, h):
    # TODO: Compute HC centrality for every vertex in h and store it in g.vdata
    Graph_i = {}
    for v in range(g.n):
        a = str(v)
        vert_edg = set([str(v) for v in g.vertex_edges(v)])
        Graph_i[a] = vert_edg
    
    result = []
    for i in range(g.n):
        dis = lambda x: shortest_path(Graph_i,str(i),str(x))
        lists = list(map(dis,h))
        total = sum(lists)
        inv = 1./total
        g.vdata[i] = inv
    return g.vdata

#code for help shortest_pach(graph,strat,goal) function
def bfs_paths(graph,start,goal):
    queue = [(start,[start])]
    while queue:
        (vertex,path) = queue.pop(0)
        for n in graph[vertex] - set(path):
            if n == goal:
                yield path + [n]
            else:
                queue.append((n,path+[n]))

#code for help compute(g,h) function
def shortest_path(graph,start,goal):
    if start == goal:
        return 0
    try:
        path = next(bfs_paths(graph, start, goal))
        return len(path)-1
    except StopIteration:
        return None

