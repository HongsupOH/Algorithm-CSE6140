# print("\\begin{table*}[]\n\caption{Solution Quality and Time measurements for different Algorithms }")
s = "\\begin{table*}[]\n\caption{Solution Quality and Time measurements for different Algorithms }\n\\resizebox{\\textwidth}{!}{%\n"+\
"\\begin{tabular}{|l|l|lllllll|}\n"+\
"\hline\n"+\
"\multirow{3}{*}{}                       & Instance         & \multicolumn{1}{l|}{Cincinnati} & \multicolumn{1}{l|}{UKansasState} & \multicolumn{1}{l|}{ulysses16} & \multicolumn{1}{l|}{Atlanta} & \multicolumn{1}{l|}{Philadelphia} & \multicolumn{1}{l|}{Boston} & \multicolumn{1}{l|}{Berlin}      \\\\ \cline{2-9}\n"+\
"                                        & Dimension        & \multicolumn{1}{l|}{10}       & \multicolumn{1}{l|}{10}       & \multicolumn{1}{l|}{16}     & \multicolumn{1}{l|}{20}        & \multicolumn{1}{l|}{30}         & \multicolumn{1}{l|}{40}     & \multicolumn{1}{l|}{52}             \\\\ \cline{2-9}\n"+\
"                                        & Optimal          & \multicolumn{1}{l|}{277952} & \multicolumn{1}{l|}{62962}     & \multicolumn{1}{l|}{6859} & \multicolumn{1}{l|}{2003763}     & \multicolumn{1}{l|}{1395981}     & \multicolumn{1}{l|}{893536} & \multicolumn{1}{l|}{7542}     \\\\ \hline\n"

algorithms = {
    "BnB": "Branch and Bound",
    "Approx": "Approximation",
    "LS1": "Local Search 1",
    "LS2": "Local Search 2",
    "H1": "Hybrid 1"
}

import pandas as pd
df1 = pd.read_csv('input_sizes.csv', names=['City2', 'Size'], dtype={'City2': 'str'})
for alg in algorithms:
    df = pd.read_csv('plots/'+alg+'.csv', dtype={'City': 'str'})
    df = df.join(df1)[['City','Time','Quality','Error','Size']]
    df = df.sort_values('Size').reset_index(drop=True)
    # print(df)

    s += '\multirow{3}{*}{'+algorithms[alg]+'}       & Time (s)'
    for i in df['Time'].values[:7]:
        s += ' & ' + str(round(i,2))
    s += '\\\\\n & Sol. Qual'
    for i in df['Quality'].values[:7]:
        s += ' & ' + str(round(i,4))
    s += '\\\\ \n & Rel Error'
    for i in df['Error'].values[:7]:
        s += ' & ' + str(round(i,4))
    s += '\\\\ \hline\n'
s += '\end{tabular}}\n \\\\'
print(s)


s = "\n\\resizebox{\\textwidth}{!}{%\n"+\
"\\begin{tabular}{|l|l|lllllll|}\n"+\
"\hline\n"+\
"\multirow{3}{*}{}                       & Instance     & \multicolumn{1}{l|}{Champaign}    & \multicolumn{1}{l|}{NYC}      & \multicolumn{1}{l|}{Denver}       & \multicolumn{1}{l|}{San Francisco}    & \multicolumn{1}{l|}{UMissouri}        & \multicolumn{1}{l|}{Toronto}      & \multicolumn{1}{l|}{Roanoke}      \\\\ \cline{2-9}\n"+\
"                                        & Dimension    & \multicolumn{1}{l|}{55}           & \multicolumn{1}{l|}{68}       & \multicolumn{1}{l|}{83}           & \multicolumn{1}{l|}{99}               & \multicolumn{1}{l|}{106}              & \multicolumn{1}{l|}{109}          & \multicolumn{1}{l|}{230}          \\\\ \cline{2-9}\n"+\
"                                        & Optimal      & \multicolumn{1}{l|}{52643}        & \multicolumn{1}{l|}{1555060}  & \multicolumn{1}{l|}{100431}       & \multicolumn{1}{l|}{810196}           & \multicolumn{1}{l|}{132709}           & \multicolumn{1}{l|}{1176151}      & \multicolumn{1}{l|}{655454}       \\\\ \hline\n"

algorithms = {
    "BnB": "Branch and Bound",
    "Approx": "Approximation",
    "LS1": "Local Search 1",
    "LS2": "Local Search 2",
    "H1": "Hybrid 1"
}

import pandas as pd
df1 = pd.read_csv('input_sizes.csv', names=['City2', 'Size'], dtype={'City2': 'str'})
for alg in algorithms:
    df = pd.read_csv('plots/'+alg+'.csv', dtype={'City': 'str'})
    df = df.join(df1)[['City','Time','Quality','Error','Size']]
    df = df.sort_values('Size').reset_index(drop=True)
    # print(df)

    s += '\multirow{3}{*}{'+algorithms[alg]+'}       & Time (s)'
    for i in df['Time'].values[7:]:
        s += ' & ' + str(round(i,2))
    s += '\\\\\n & Sol. Qual'
    for i in df['Quality'].values[7:]:
        s += ' & ' + str(round(i,4))
    s += '\\\\ \n & Rel Error'
    for i in df['Error'].values[7:]:
        s += ' & ' + str(round(i,4))
    s += '\\\\ \hline\n'
s += '\end{tabular}}\n\label{table_results}\n\end{table*}'
print(s)
# print("\n\label{table_results}\n\end{table*}")