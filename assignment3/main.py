import sys
import random
import community
from copy import deepcopy
from statistics import mean
import networkx as nx
from networkx.algorithms import node_classification
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics.cluster import adjusted_rand_score

# Gets Ground truth from data supplied by file
def get_ground_truth_labels_from_graph(G):

    ground_truths = []

    for node in G.nodes():
        ground_truths.append(G.node[node]['value'])
    
    return ground_truths

def calculate_nmi_ars(truth, prediction):
    
    nmi = normalized_mutual_info_score(truth, prediction, 'arithmetic')
    ars = adjusted_rand_score(truth, prediction)
    #print('NMI:', nmi, 'ARS:', ars)
    return nmi , ars

def calculate_node_classification_accuracy(G, label, ground_truths, method):

    nmi_list = []
    ars_list = []

    for i in range(10):
        
        if method == 'harmonic':
            predictions = node_classification.harmonic_function(G, label_name=label)
        else:
            predictions = node_classification.local_and_global_consistency(G, label_name=label)
        
        nmi, ars = calculate_nmi_ars(ground_truths, predictions)
        nmi_list.append(nmi)
        ars_list.append(ars)
    
    average_nmi = round(mean(nmi_list), 2)
    average_ars = round(mean(ars_list), 2)
    
    print('Average NMI:', average_nmi)
    print('Average ARS:', average_ars)

    return average_nmi, average_ars

option = sys.argv[1]
file_name = sys.argv[2]

print('Assignment 3 - Node Classification\n')

if option == 'a':
    print('Real Data -', file_name)

    # Checks to See weather to start array by 0 or 1, some Matlab BS Crap in the data
    matlab_bs = False
    if (('strike' in file_name) or ('karate' in file_name) or ('polblog' in file_name)):
        matlab_bs = True
    
    G = nx.read_gml(file_name, label='id')
    labels_truth = get_ground_truth_labels_from_graph(G)
    number_of_nodes = nx.number_of_nodes(G)
    #print('Ground Truth Labels:\n', labels_truth)
    print('\nNumber of Nodes in Graph:', number_of_nodes)

    drop_factors = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]

    for drop_factor in drop_factors:
        
        print('\nNode Prediction when', int(drop_factor*100), r'% of nodes are dropped')
        g = deepcopy(G)

        for node in random.sample(g.nodes(), int(number_of_nodes*drop_factor)):
            del g.node[node]['value']
        
        calculate_node_classification_accuracy(g, 'value', labels_truth, 'harmonic')
        


elif option == 'b':
    print('GNC Data - ', file_name)
elif option == 'c':
    print('Synthetic Data - No File')