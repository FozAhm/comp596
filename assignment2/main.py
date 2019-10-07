import sys
import networkx as nx
import pickle as pkl

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'true':
        return True
    elif s == 'False':
         return False
    elif s == 'false':
        return False
    else:
         raise ValueError("Cannot covert {} to a bool".format(s))

option = sys.argv[1]
file_name = sys.argv[2]

if option == 'a':
    print('Real Data')
    G = nx.read_gml(file_name, label='id')
elif option == 'b':
    print('GNC Data')

    data = []
    with open(file_name + '.ally', 'rb') as f:
        data.append(pkl.load(f, encoding='latin1'))
    with open(file_name + '.graph', 'rb') as f:
        data.append(pkl.load(f, encoding='latin1'))
    
    print('All y data: ', data[0])
    print('Graph: ', data[1])

elif option == 'c':
    print('Synthetic Data')
else:
    print('Wrong Option Selected')