import sys
import random
import community
import networkx as nx
import pickle as pkl
import numpy as np
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community import k_clique_communities
from networkx.algorithms.community import LFR_benchmark_graph
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics.cluster import adjusted_rand_score

# First Argument Should Specify what type of data is being tested: a = real, b = gcn, c = synthetic
# Second Argument is File Path, for option c just put anything (ie: 'test')

# Converts a Binary One Hot Feature Array to a Number
def convert_onehot_to_integer(array):
    
    return np.where(array == 1)[0][0]

# Converts GCN Data to a NetworkX Graph, removing nodes along with related edges which did not have a ground truth label in y 
def convert_to_networkx(labels, graph):
    G = nx.Graph()

    num_of_groud_truths = len(labels)

    for node, neighbours in graph.items():
        
        if node < num_of_groud_truths:
            G.add_node(node, value=convert_onehot_to_integer(labels[node]))

    for node, neighbours in graph.items():
        for neighbour in neighbours:

            if ((node < num_of_groud_truths) and (neighbour < num_of_groud_truths)):
                G.add_edge(node, neighbour)
    
    return G

def get_ground_truth_labels_from_graph(G):

    ground_truths = []

    for node in G.nodes():
        ground_truths.append(G.node[node]['value'])
    
    return ground_truths

def get_labels_from_community(communities, num_of_nodes, matlab_bs=False):

    i = 0
    labels = list(range(num_of_nodes))
    for community in communities:
        for node in community:
            
            if matlab_bs:
                labels[node-1] = i
            else:
                labels[node] = i
        
        i += 1
    
    return labels

def get_predicted_label_from_louvain(communities, num_of_nodes, matlab_bs=False):
    
    labels = list(range(num_of_nodes))
    num_of_communities = -1
    
    for node, community in communities.items():
        
        if matlab_bs:
            labels[node-1] = community
        else:
            labels[node] = community
        
        if community > num_of_communities:
            num_of_communities = community
    
    return labels, num_of_communities

def clauset(G, number_of_nodes, matlab_bs=False):

    print('\nClauset Algorithm')
    clauset = greedy_modularity_communities(G)
    #print('Clauset Communities:\n', clauset)
    print('Number of Communities with Clauset:', len(clauset))
    clauset_labels_predicted = get_labels_from_community(clauset, number_of_nodes, matlab_bs)
    #print('Clauset Truth Labels:\n', clauset_labels_predicted)

    return clauset_labels_predicted

def louvain(G, number_of_nodes, matlab_bs=False):

    print('\nLouvain Algorithm')
    louvain = community.best_partition(G)
    #print('Louvain Communities:\n', louvain)
    louvain_labels_predicted, num_of_communities_louvain = get_predicted_label_from_louvain(louvain, number_of_nodes, matlab_bs)
    print('Number of Communities with Louvain:', num_of_communities_louvain)
    #print('Louvain Truth Labels:\n', louvain_labels_predicted)

    return louvain_labels_predicted

def k_clique(G, number_of_nodes, matlab_bs=False):

    print('\nK Clique Algorithm')
    k_clique = list(k_clique_communities(G, 4))
    #print('K-Clique:\n', k_clique)
    print('Number of Communities with K-Clique:', len(k_clique))
    k_clique_labels_predicted = get_labels_from_community(k_clique, number_of_nodes, matlab_bs)
    #print('K-Clique Truth Labels:\n', k_clique_labels_predicted)

    return k_clique_labels_predicted

def calculate_nmi_ars(truth, prediction):
    
    nmi = normalized_mutual_info_score(truth, prediction, 'arithmetic')
    ars = adjusted_rand_score(truth, prediction)
    print('NMI:', nmi, 'ARS:', ars)
    return nmi , ars

def calculate_community(G, number_of_nodes, labels_truth, matlab_bs=False):

    clauset_labels_predicted = clauset(G, number_of_nodes, matlab_bs)
    clauset_nmi_ars = calculate_nmi_ars(labels_truth, clauset_labels_predicted)

    louvain_labels_predicted = louvain(G, number_of_nodes, matlab_bs)
    louvain_nmi_ars = calculate_nmi_ars(labels_truth, louvain_labels_predicted)

    k_clique_labels_predicted = k_clique(G, number_of_nodes, matlab_bs)
    k_clique_nmi_ars = calculate_nmi_ars(labels_truth, k_clique_labels_predicted)


# Loading command line arguments
option = sys.argv[1]
file_name = sys.argv[2]


if option == 'a':
    print('\nReal Data -', file_name)

    # Checks to See weather to start array by 0 or 1, some Matlab BS Crap in the data
    matlab_bs = False
    if (('strike' in file_name) or ('karate' in file_name) or ('polblog' in file_name)):
        matlab_bs = True

    G = nx.read_gml(file_name, label='id')
    labels_truth = get_ground_truth_labels_from_graph(G)
    number_of_nodes = nx.number_of_nodes(G)
    #print('Ground Truth Labels:\n', labels_truth)
    print('\nNumber of Nodes in Graph:', number_of_nodes)

    calculate_community(G, number_of_nodes, labels_truth, matlab_bs)

elif option == 'b':
    print('GNC Data - ', file_name)

    # Unpickle and load data
    with open(file_name + 'ally', 'rb') as f:
        labels = pkl.load(f, encoding='latin1')
    with open(file_name + 'graph', 'rb') as f:
        graph = pkl.load(f, encoding='latin1')
    
    # For Testing and Debugging
    #print('Labels:\n', labels)
    #print('First Label', convert_onehot_to_integer(labels[0]))
    #print('Second Label', convert_onehot_to_integer(labels[1]))
    #print('Third Label', convert_onehot_to_integer(labels[2]))
    #print('Graph: ', graph)
    #print('Size of Labels:', len(labels))

    G = convert_to_networkx(labels, graph)
    labels_truth = get_ground_truth_labels_from_graph(G)
    number_of_nodes = nx.number_of_nodes(G)
    #print('Ground Truth Labels:\n', labels_truth)
    print('\nNumber of Nodes in Graph:', number_of_nodes)

    calculate_community(G, number_of_nodes, labels_truth)

elif option == 'c':
    print('Synthetic Data - No File')

    n = 1000
    tau1 = 3
    tau2 = 1.5
    mu = 0.5
    average_degree = 5
    minimum_community=20

    G = LFR_benchmark_graph(n, tau1, tau2, mu, average_degree, min_community=minimum_community)
    #print(G.nodes[0])
    communities = {frozenset(G.nodes[v]['community']) for v in G}
    #print('Communities:\n', communities)
    print('Number of Ground Turth Communities:', len(communities))
    labels_truth = get_labels_from_community(communities, n)
    #print('Ground Truth Labels:\n', labels_truth)

    calculate_community(G, n, labels_truth)

else:
    print('Wrong Option Selected')