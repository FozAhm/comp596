import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
import matplotlib.pyplot as plt
import collections
import powerlaw
import numpy as np
import sys
import csv
import time

start_time = time.time()

print('Graph Analysis...')

data_location = sys.argv[1]
read_format = sys.argv[2]
option = sys.argv[3]

graph_name = data_location.split('/')[-1]

if read_format == 'gml':
    G = nx.read_gml(data_location)
elif read_format == 'gpkl':
    G = nx.read_gpickle(data_location)

print("--- Graph Load Time ---\n--- %s seconds ---" % (time.time() - start_time))

option_start_time = time.time()

if option == 'numnodes':
    print('Number of Nodes:', len(G))
elif option == 'numedges':
    print('Number of Edges:', G.size())
elif option == 'degreedist':
    print('Degree Distribution')
    title = 'Degree Distribution for ' + graph_name
    degree_list = nx.degree_histogram(G)
    results = powerlaw.Fit(degree_list, discrete=True)
    print('Power Law Alpha:', results.power_law.alpha)

    x = np.arange(1, len(degree_list)+1)
    plt.title(title)
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.xscale('log')
    plt.yscale('log')
    plt.plot(x, degree_list, 'bo')
    plt.grid(True)
    save_name = graph_name + '_degree_dist.png' 
    plt.savefig(save_name)
elif option == 'community':
    print('Community Detection')
    c = list(greedy_modularity_communities(G))
    print('Number of communities:', len(c))
    print('Community 1:', c[0])
    print('Community 2:', c[1])
elif option == 'degreecorrel':
    print('Degree Correlation')
    r = nx.degree_pearson_correlation_coefficient(G)
    print('r:', r)
elif option == 'gcc':
    print('Global Clustering Coeffecient')
    gcc = nx.average_clustering(G)
    print('gcc:', gcc)
else:
    print('Wrong Option')

print("--- Total Option Execution Time ---\n--- %s seconds ---" % (time.time() - option_start_time))

print("--- Total Program Execution Time ---\n--- %s seconds ---" % (time.time() - start_time))
