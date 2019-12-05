import networkx as nx
import sys
import csv

print('Graph Generation...')

data_location = sys.argv[1]

all_files = [
    'all_nodes.csv',
    'all_push.csv',
    'all_fork.csv',
    'all_watch.csv'
]

G = nx.Graph()

for file in all_files:
    
    file_path = data_location + file
    
    with open(file_path) as csv_file:

        print('Going through file:', file)
        
        csv_reader = csv.reader(csv_file, delimiter=',')
    
        if file == 'all_nodes.csv':
            for row in csv_reader:
                G.add_node(row[0], type=row[1])
        
        elif file == 'all_push.csv':
            for row in csv_reader:
                G.add_edge(row[0], row[1], type='Push', weight=int(row[2]))
        
        elif file == 'all_fork.csv':
            for row in csv_reader:
                G.add_edge(row[0], row[1], type='Fork', weight=int(row[2]))
        
        elif file == 'all_watch.csv':
            for row in csv_reader:
                G.add_edge(row[0], row[1], type='Watch', weight=int(row[2]))

print('Number of Nodes:', len(G))
print('Number of Edges:', G.size())

#nx.write_gml(G, "github.gml")
#nx.write_gpickle(G, "github.gpickle")
nx.write_gexf(G, "github.gexf")