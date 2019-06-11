import seaborn as sns
import numpy as np
import pandas as pd


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
    plt.rcParams['figure.figsize'] = 16,8
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
        # print(round(ts[-1]/1000, 2), int(w), round(error[-1]/100, 6))
        error = np.array(error)
        return {
            'time': np.array(ts), 
            'error': error, 
            'w': ws
        }


def run(alg):
    traces = {}
    for i in range(20):
        traces[i] = fill_for('Toronto', alg, 600.0, float(i))

    s = []
    step = 2
    for i in range(0,16,step):
        s.append([i,i+step, i+step/2])

    bins = {}
    for bin in s:
        bins[bin[2]] = []

    v = []
    sx = []
    sy = []
    for seed in range(20):
        ts = traces[seed]['time']
        errors = traces[seed]['error']
        sx += list(errors-1)
        sy += list(ts/1000)
        for bin in s:
            a = errors < bin[1]
            b = errors >= bin[0]
            c = a*b
            # c = a
            bins[bin[2]] += list(ts[c])
            for t in ts[c]:
                v.append([t, bin[2]])
    v = np.array(v)

    df = pd.DataFrame(columns=['Time', 'Error %'])
    df['Time'] = v[:, 0]/1000
    df['Error %'] = v[:, 1]
    df2 = df.groupby('Error %').agg('median').reset_index(drop=False)
    print(df2)
    plt = set_plot()
    ax = plt.gca()
    for i in range(df2.shape[0]):
        ax.text(i-0.2,df2.values[i][1], str(int(df2.values[i][1])),fontsize=24)
    sns.boxplot(x="Error %", y="Time", data=df, ax=ax, color='#CCCCFF')
    # sns.scatterplot(sx,sy,ax=ax,s=50)
    plt.savefig("plots/"+alg+"_error_time_boxplot_Toronto.pdf", bbox_inches='tight', transparent=True,dpi=100 )
    plt.clf()

run('LS1')
run('LS2')
