import numpy as np
import seaborn as sns
import sys
if len(sys.argv) < 2:
    print("Usage")
    print("python execute.py <BnB | Approx | LS1 | LS2 | H1>")
    print("Example: ")
    print("python execute.py BnB")
    exit(0)
alg = sys.argv[1]
if alg not in ['BnB', 'Approx', 'LS1', 'LS2' ,'H1']:
    print("Usage")
    print("python execute.py <BnB | Approx | LS1 | LS2 | H1>")
    print("Example: ")
    print("python execute.py BnB")
    exit(0)

def set_plot():
    import matplotlib.pyplot as plt
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['font.size'] = 32
    plt.rcParams['ytick.labelsize'] = 26
    plt.rcParams['xtick.labelsize'] = 24
    plt.rcParams['legend.fontsize'] = 24
    plt.rcParams['lines.markersize'] = 8
    plt.rcParams['axes.titlesize'] = 28
    plt.rcParams['axes.labelsize'] = 32
    plt.rcParams['axes.edgecolor'] = '#f0f0f0'
    plt.rcParams['axes.edgecolor'] = '#f0f0f0'
    plt.rcParams['axes.linewidth'] = 3.0
    plt.rcParams['axes.grid'] = False
    plt.rcParams['grid.alpha'] = 0.7
    plt.rcParams['grid.color'] = '#f0f0f0'
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['legend.framealpha'] = 0.4
    plt.rcParams['legend.numpoints'] = 1
    plt.rcParams['legend.scatterpoints'] = 1
    plt.rcParams['figure.figsize'] = 16, 8
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().get_xaxis().tick_bottom()
    plt.gca().get_yaxis().tick_left()
    plt.tick_params(axis='both', which='major', bottom=True, top=False, labelbottom=True, left=True,
                    right=False, labelleft=True, length=10, width=4, direction='inout',  color='#525252')

    return plt


optimals = {}
with open('optimal_solutions.csv', "r") as opt:
    for line in opt.readlines():
        line = line.replace('\n', '')
        city, opt_weight = line.split(',')
        optimals[city] = float(opt_weight)

dimensions = {}
with open('input_sizes.csv', "r") as opt:
    for line in opt.readlines():
        line = line.replace('\n', '')
        city, dimension = line.split(',')
        dimensions[city] = int(dimension)


traces = {}


def fill_for(inst, alg, time, seed):
    trace_file = inst+'_'+alg+'_'+str(time)+'_'+str(seed)+'.trace'
    with open('output/'+trace_file, 'r') as trace_file:
        error = []
        ts = []
        act = optimals[inst]
        ws = []
        for line in trace_file.readlines():
            line = line.replace('\n', '')
            t, w = line.split(' ')
            t = float(t)*1000
            w = float(w)
            ts.append(t)
            error.append(100*(w-act)/act)
            ws.append(w)
        print(round(ts[-1]/1000,2),int(w),round(error[-1]/100,6))
        traces[inst] = {'time': ts, 'error': error, 'w': ws}
        return "{0},{1},{2},{3}\n".format(inst,round(ts[-1]/1000,2),int(w),round(error[-1]/100,6))


with open('executions_'+alg+'.csv', 'r') as f:
    data = "City,Time,Quality,Error\n"
    for line in f.readlines():
        line = line.replace('\n', '')
        line = line.replace('\r', '')
        inst, alg, time, seed = line.split(',')
        data += fill_for(inst, alg, float(time), float(seed))
    with open('plots/'+alg+'.csv', 'w') as fi:
        fi.write(data)

plt = set_plot()
ax = plt.gca()
dimensions_sort = sorted(dimensions.items(), key=lambda kv: kv[1])
for (x, d) in dimensions_sort:
    ts, error = traces[x]['time'], traces[x]['error']
    sns.lineplot(ts, error, ax=ax, label=x+' N='+str(dimensions[x]), linewidth=8)

ax.set_ylabel('Error %')
ax.set_xlabel('Time (ms)')
ax.set_xlim([10, 10**10])
ax.set_xscale('log')
plt.legend()
plt.rcParams['legend.fontsize'] = 24
plt.savefig("plots/"+alg+"_D_Comparison.pdf", bbox_inches='tight', transparent=True)
plt.clf()


if alg in ['LS1', 'LS2', 'BnB', 'H1']:
    es = []
    ds = []
    t = []
    for (x, d) in dimensions_sort:
        ts, error = traces[x]['time'], traces[x]['error']
        if d < 20:
            continue
        for i in range(len(error)):
            if error[i] < 10:
                t.append(ts[i])
                ds.append(d)
                break


    plt = set_plot()
    ax = plt.gca()
    if(len(t)>0):
        z = np.polyfit(ds, np.log10(t), 1)
        p = np.poly1d(z)
        print(p(ds[0]))
        y = [10**p(i) for i in range(1,250)]
        sns.lineplot(range(1,250), y,ax=ax,linewidth=4)
        sns.scatterplot(ds, t, ax=ax,marker='x',s=300)
        ax.set_ylabel('Time (ms)')
        ax.set_xlabel('Dimension')
        ax.set_yscale('log')
        ax.set_xlim([0,250])
        ax.set_ylim([1,10**6])
        plt.rcParams['legend.fontsize'] = 24
        plt.savefig("plots/"+alg+"_10pct.pdf", bbox_inches='tight', transparent=True)
        plt.clf()

if alg in ['Approx']:
    print(traces)
    print(dimensions)
    x = []
    y = []
    for i in traces:
        y.append(traces[i]['time'][-1])
        x.append(dimensions[i])
    plt = set_plot()
    ax = plt.gca()
    sns.scatterplot(x,y,ax=ax,label='Running Time',s=300,marker='x',color='black')
    x = np.array(range(1,250))
    y2 = 1.5*x*x*np.log(x)*10**-2
    sns.lineplot(range(1,250), y2,ax=ax, label='O(n*n*log(n))',linewidth=4)
    ax.set_xlabel('# Nodes')
    ax.set_ylabel('Time (ms)')
    ax.set_xlim([0,250])
    plt.legend()
    plt.rcParams['legend.fontsize'] = 36
    plt.savefig("plots/"+alg+"_TimeComplexity.pdf", bbox_inches='tight', transparent=True)
    plt.clf()



import pandas as pd
input_sizes = pd.read_csv('input_sizes.csv', names=['City','Size'])
input_sizes = input_sizes.sort_values('Size').reset_index(drop=True)
x = []
y = []
d = []
for i in input_sizes['City'].values:
    y.append(round(traces[i]['error'][-1],2))
    x.append(i)
    d.append(dimensions[i])
plt = set_plot()
ax = plt.gca()
df = input_sizes
df['Error %'] = y
sns.barplot(x='Error %', y='City', color='#CCCCFF', data=df,ax=ax)
for i in range(len(x)):
    ax.text(y[i], i+0.25, str(y[i]),fontsize=22)
ax.set_ylabel('')
ax.set_xlim([0,max(y)*1.2])
plt.savefig("plots/"+alg+"_Error.pdf", bbox_inches='tight', transparent=True)
