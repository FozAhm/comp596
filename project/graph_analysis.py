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
graph_name_noextension = graph_name.split('.')[0]

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
    degree_list = nx.degree_histogram(G)
    results = powerlaw.Fit(degree_list, discrete=True)
    alpha = results.power_law.alpha
    print('Power Law Alpha:', alpha)
    title = 'Degree Distribution for ' + graph_name_noextension + '\nPower Law Alpha Value: ' + str(alpha) 

    x = np.arange(1, len(degree_list)+1)
    plt.title(title)
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.xscale('log')
    plt.yscale('log')
    plt.plot(x, degree_list, 'bo')
    plt.grid(True)
    save_name = graph_name.replace('.', '_') + '_degree_dist.png' 
    plt.savefig(save_name)
elif option == 'community':
    print('Community Detection')
    c = list(greedy_modularity_communities(G))
    print('Number of communities:', len(c))
    file_name = graph_name_noextension + '_community.txt' 
    f = open(file_name, 'a')
    f.write('Community 1')
    f.write(c[0])
    f.write('Community 2')
    f.write(c[1])
    f.close()
elif option == 'degreecorrel':
    print('Degree Correlation')
    r = nx.degree_pearson_correlation_coefficient(G, weight='weight')
    print('r:', r)
elif option == 'gcc':
    print('Global Clustering Coeffecient')
    gcc = nx.average_clustering(G, weight='weight')
    print('gcc:', gcc)
elif option == 'avgdeg':
    print('Average Degree')
    degrees = list(G.degree(weight='weight'))
    sum_of_degrees = 0
    highest_degree = 0
    highest_degree_node = G.nodes['hartbeatnt']  #Just to initialize
    for key,value in degrees:
        sum_of_degrees += value
        if value > highest_degree:
            highest_degree = value
            highest_degree_node = key
    avgdeg = sum_of_degrees/len(G)
    print(avgdeg)
    print('Node with Highest Degree:', highest_degree, highest_degree_node)
    print(G.nodes[highest_degree_node])
    print('First Edge')
    print(list(G.edges(highest_degree_node))[0])
    print('Second Edge')
    print(list(G.edges(highest_degree_node))[1])
elif option == 'lcc':
    print('Largest Connected Component')
    largest_cc = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    print('Percentage of Nodes in the LCC:', len(largest_cc)/len(G))
    lcc_name = graph_name_noextension + '_lcc.gpickle'
    nx.write_gpickle(G, lcc_name)
    print('LCC Saved')
elif option == 'meansp':
    print('Mean Shortest Path of LCC')
    largest_cc = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    print('LCC Obtained...')
    meansp = nx.average_shortest_path_length(largest_cc)
    print('MSP:', meansp)
else:
    print('Wrong Option')

print("--- Total Option Execution Time ---\n--- %s seconds ---" % (time.time() - option_start_time))

print("--- Total Program Execution Time ---\n--- %s seconds ---" % (time.time() - start_time))
