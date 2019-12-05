import networkx as nx
import sys
import csv
import time

start_time = time.time()

print('Graph Analysis...')

data_location = sys.argv[1]

G = nx.read_gml(data_location)
print('Number of Nodes:', len(G))
print('Number of Edges:', G.size())

print("--- %s seconds ---" % (time.time() - start_time))
