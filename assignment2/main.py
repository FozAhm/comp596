import sys
import networkx as nx

file_name = sys.argv[1]

G = nx.read_gml(file_name, label='id')

print('Test')