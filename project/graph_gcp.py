import networkx as nx
import sys
import csv
import os
import json

print('Graph Generation...')

data_location = sys.argv[1] # Should be /home/ubuntu/comp596/project/gcp/
option = sys.argv[2] # Shlould be gml or gpkl

data_directory = os.fsencode(data_location)

G = nx.Graph()

for file in os.listdir(data_directory):
    filename = os.fsdecode(file)
    file_path = data_location + filename

    print('Looking through', file_path, '...')

    if 'csv' in filename:
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            if 'authors' in filename:
                for row in csv_reader:
                    G.add_node(row[0], type='user')
            elif 'repo' in filename:
                for row in csv_reader:
                    G.add_node(row[0], type='repo')
    elif 'json' in filename:
        with open(file_path, 'rt', encoding='utf-8') as f:
            for line in f:
                event = json.loads(line)
                if event['email'] != '':
                    G.add_edge(event['email'], event['r_name'], weight=int(event['total']))

print('Number of Nodes:', len(G))
print('Number of Edges:', G.size())

if option == 'gml':
    nx.write_gml(G, "github_gcp.gml")
elif option == 'gpkl':
    nx.write_gpickle(G, "github_gcp.gpickle")