import seaborn as sns
import numpy as np
from scipy.special import factorial

def set_plot():
    import matplotlib.pyplot as plt
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['font.size'] = 32
    plt.rcParams['ytick.labelsize'] = 26
    plt.rcParams['xtick.labelsize'] = 24
    plt.rcParams['legend.fontsize'] = 18
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

arr = np.array(range(25))
f = factorial(arr)/10**10
f= f/(365*86400)
plt = set_plot()
ax = plt.gca()
sns.lineplot(range(25),f,ax=ax,linewidth=6)
sns.scatterplot(range(25), f, s=300)
ax.set_yscale('symlog')
ax.set_ylabel('# Years')
ax.set_xlabel('# Nodes')
plt.ylim([-1, 10**7])
plt.savefig('plots/Complexity.pdf', bbox_inches='tight', transparent=True)
plt.show()
print(f)
