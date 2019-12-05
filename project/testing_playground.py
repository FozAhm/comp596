print('This is a testing playground')

import networkx as nx

G = nx.Graph()

G.add_node('Test1', type='user')
G.add_node('Test2', type='repo')

print(G.nodes['Test1'])
print(G.nodes.data())

G.add_edge('Test1', 'Test2', type='watch', weight=1)

print(G.get_edge_data('Test1', 'Test2'))