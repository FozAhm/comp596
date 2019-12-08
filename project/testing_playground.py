print('This is a testing playground')

import networkx as nx
import sys

data_location = sys.argv[1]
print(data_location.split('/')[-1])

G = nx.Graph()

G.add_node('Test1', type='user')
G.add_node('Test2', type='repo')

print(G.nodes['Test1'])
print(G.nodes.data())

G.add_edge('Test1', 'Test2', type='watch', weight=1)

print(G.get_edge_data('Test1', 'Test2'))

lst = [(4, 11), (5, 22), (6, 33)]

for key,value in lst:
    print(value)