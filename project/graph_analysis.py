import networkx as nx
import matplotlib.pyplot as plt
import collections
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

if option == 'numnodes':
    print('Number of Nodes:', len(G))
elif option == 'numedges':
    print('Number of Edges:', G.size())
elif option == 'degreehist':
    #degree_list = nx.degree_histogram(G)
    #print(degree_list)

    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    # print "Degree sequence", degree_sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)
    plt.savefig('degree_dist2.png')

print("--- Total Execution Time ---\n--- %s seconds ---" % (time.time() - start_time))
