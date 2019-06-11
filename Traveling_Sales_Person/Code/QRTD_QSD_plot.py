
# coding: utf-8

# In[178]:


import numpy as np
import pandas as pd
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


# In[193]:


def run(CITY,ALG):
    markers = ['o', '+', 'x', 'D', '*', 's', '2']
    T =[]
    E = []
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
                t = float(t)
                w = float(w)
                e = 100*(w-act)/act
                ts.append(t)
                error.append(e)
                ws.append(w)
                T.append(t)
                E.append(e)
            error = np.array(error)
            traces[seed] = {'time': np.array(ts), 'error': error, 'w': ws, '5%': np.array(error<5, dtype=int)}
            return (round(ts[-1]/1000,2),int(w),round(error[-1]/100,6))

    finals = []
    for i in range(10):
        finals.append(fill_for(CITY, ALG, 600, i))
    finals = np.array(finals)
    df = pd.DataFrame(columns=['Time', 'Error'])
    df['Time'] = T
    df['Error'] = E
    m = 0
    plt = set_plot()
    for i in range(5,26,5):
        d = df
        d = d[d['Error']<=i]
        c = d.shape[0]
        if c == 0:
            continue
        ts = []
        ps = []
        for t in range(0,601,30):
            d2 = d[d['Time']<=t]
            ps.append(d2.shape[0]/c)
            ts.append(t)
        plt.plot(ts,ps)
        plt.scatter(ts,ps, label="Error <"+str(i)+"%", marker=markers[m])
        m+=1
    plt.legend()
    plt.xlabel('Time(T)')
    plt.ylabel('P(Time<T/Error<E)')
    # plt.savefig("plots/"+ALG+"_QRTD.png", bbox_inches='tight', transparent=False)
    plt.savefig("plots/"+ALG+"_QRTD.pdf", bbox_inches='tight', transparent=False)
    plt.clf()

    m = 0
    plt = set_plot()
    es = []
    ps = []
    for i in [0, 10, 20, 30, 50, 80, 300, 600]:
        d = df
        d = d[d['Time']<=i]
        c = d.shape[0]
        if c == 0:
            continue
        es = []
        ps = []
        for e in range(0, 121, 20):
            d2 = d
            d2 = d2[d2['Error']<=e]
            ps.append(d2.shape[0]/c)
            es.append(e)
        plt.plot(es,ps)
        plt.scatter(es,ps,label="Time <"+str(i)+"s", marker=markers[m])
        m+=1
    plt.legend()
    plt.ylim([0,1])
    plt.xlabel('Error(E)')
    plt.ylabel('P(Error<E/Time<T)')
    # plt.savefig("plots/"+ALG+"_SQD.png", bbox_inches='tight', transparent=False)
    plt.savefig("plots/"+ALG+"_SQD.pdf", bbox_inches='tight', transparent=False)
    plt.clf()


# In[199]:


run('Toronto','LS1')


# In[200]:


run('Toronto','LS2')

