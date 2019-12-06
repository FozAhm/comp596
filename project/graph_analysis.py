import networkx as nx
import matplotlib.pyplot as plt
import collections
import numpy as np
import sys
import csv
import time

start_time = time.time()

print('Graph Analysis...')

data_location = sys.argv[1]
read_format = sys.argv[2]
option = sys.argv[3]

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
elif option == 'degreehist':
    degree_list = nx.degree_histogram(G)
    #print(degree_list)

    x = np.arange(1, len(degree_list)+1)

    plt.plot(x, degree_list, 'bo')
    plt.savefig('photos/degree_dist.png')
else:
    print('Wrong Option')

print("--- Total Option Execution Time ---\n--- %s seconds ---" % (time.time() - option_start_time))

print("--- Total Program Execution Time ---\n--- %s seconds ---" % (time.time() - start_time))
