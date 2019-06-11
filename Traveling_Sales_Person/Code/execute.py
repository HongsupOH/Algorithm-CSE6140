import os
from subprocess import *
import sys
if len(sys.argv) < 2:
    print("Usage")
    print("python error_plot.py <BnB | Approx | LS1 | LS2 | H1>")
    print("Example: ")
    print("python error_plot.py BnB")
    exit(0)
alg = sys.argv[1]
if alg not in ['BnB', 'Approx', 'LS1', 'LS2' ,'H1']:
    print("Usage")
    print("python error_plot.py <BnB | Approx | LS1 | LS2 | H1>")
    print("Example: ")
    print("python error_plot.py BnB")
    exit(0)

processes = []
with open('executions_'+alg+'.csv', 'r') as f:
    for line in f.readlines():
        line = line.replace('\n','')
        line = line.replace('\r','')
        inst,alg,time,seed = line.split(',')
        s = 'python main.py'+\
            ' -inst DATA/'+inst+'.tsp'+\
            ' -alg '+alg+\
            ' -time '+time+\
            ' -seed '+seed
        print(s)
        processes.append(Popen(s, shell=True))

exitcodes = [p.wait() for p in processes]
print(exitcodes)