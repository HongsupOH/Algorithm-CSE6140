import random
import sys
import getopt
from algorithms import *
from helpers import *

if len(sys.argv[1:]) < 6:
    print("Incorrect Parametrs Passed")
    print("Refer Below")
    print("python main.py -inst DATA/small.tsp -alg BnB -time 10")
    exit(0)

inst = sys.argv[2]
alg = sys.argv[4]
time = int(sys.argv[6])

if len(sys.argv[1:]) == 6:
    seed = 1000
    output_file = '_'+alg+'_'+str(time)+'.sol'
    tour_file = '_'+alg+'_'+str(time)+'.tour'
    trace_file = '_'+alg+'_'+str(time)+'.trace'

if len(sys.argv[1:]) == 8:
    seed = int(sys.argv[8])
    output_file = '_'+alg+'_'+str(time)+'_'+str(seed)+'.sol'
    tour_file = '_'+alg+'_'+str(time)+'_'+str(seed)+'.tour'
    trace_file = '_'+alg+'_'+str(time)+'_'+str(seed)+'.trace'

if alg not in ['BnB', 'Approx', 'LS1', 'LS2', 'H1']:
    print("Invalid Algorithm passed")
    exit(0)

if alg in ['BnB', 'Approx', 'H1']:
    seed = 1000
    output_file = '_'+alg+'_'+str(time)+'.sol'
    tour_file = '_'+alg+'_'+str(time)+'.tour'
    trace_file = '_'+alg+'_'+str(time)+'.trace'

random.seed(int(seed))
np.random.seed(int(seed))
timelimit = time
graph = Graph(inst)
output_file = 'output/' + graph.city + output_file
tour_file = 'output/' + graph.city + tour_file
trace_file = 'output/' + graph.city + trace_file

import os
if 'output' not in os.listdir('./'):
    os.mkdir('./output')

if alg == 'BnB':
    solution = BranchAndBound(graph, timelimit, seed).get_results()
elif alg == 'Approx':
    solution = Approx(graph, timelimit, seed).get_results()
elif alg == 'LS1':
    solution = LocalSearch1(graph, timelimit, seed).get_results()
elif alg == 'LS2':
    solution = LocalSearch2(graph, timelimit, seed).get_results()
elif alg == 'H1':
    solution = Hybrid1(graph, timelimit, seed).get_results()
elif alg == 'H2':
    solution = Hybrid2(graph, timelimit, seed).get_results()
else:
    print("Invalid Algorithm passed")
    exit(0)

with open(tour_file, 'w') as f:
    f.write(solution[0])
with open(trace_file, 'w') as f:
    f.write(solution[1])
with open(output_file, 'w') as f:
    if len(solution[2]['tour']):
        f.write(str(solution[2]['weight'])+'\n')
        o = ''
        for c in solution[2]['tour']:
            o += str(c+1) + ','
        f.write(o[:-1]+'\n')
