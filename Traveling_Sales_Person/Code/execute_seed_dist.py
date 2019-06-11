
import os
from subprocess import *
import sys
for inst in ['Atlanta', 'berlin52', 'Boston', 'Champaign', 'Cincinnati', 'Denver', 'NYC', 'Philadelphia', 'Roanoke', 'SanFrancisco', 'Toronto', 'UKansasState', 'ulysses16', 'UMissouri']:
    processes = []
    alg = 'LS1'
    for seed in range(10):
        s = 'python main.py'+\
            ' -inst DATA/'+inst+'.tsp'+\
            ' -alg '+alg+\
            ' -time 600'+\
            ' -seed '+str(seed)
        print(s)
        processes.append(Popen(s, shell=True))

    alg = 'LS2'
    for seed in range(10):
        s = 'python main.py'+\
            ' -inst DATA/'+inst+'.tsp'+\
            ' -alg '+alg+\
            ' -time 600'+\
            ' -seed '+str(seed)
        print(s)
        processes.append(Popen(s, shell=True))
    exitcodes = [p.wait() for p in processes]
    print(exitcodes)