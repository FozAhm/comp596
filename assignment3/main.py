import sys
import csv
import random
import community
import numpy as np
import pickle as pkl
import networkx as nx
from copy import deepcopy
from statistics import mean
import matplotlib.pyplot as plt
from networkx.algorithms import node_classification
from networkx.algorithms.community import LFR_benchmark_graph
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import normalized_mutual_info_score

# HOW TO RUN - What Command Line Options to Use Each - White Spaces are the Delimiters
# the First Variable defines what type of data you are working with: 'a' for real-classic, 'b' for gcm data, 'c' for synthetic 
# The Second Variable is the File Path, please only enter file path without file extension for GCN data, put anything for option c
# The Third Variable is the name you want to give to the data you running, put anything you wish
# The Fourth Variable defined what node classification algorithm to use, put 'harmonic' or 'logical'  

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

# Gets Lablels in Array corresponding to Nodes from a Nestered Community Label Arhitecture 
def get_labels_from_community(communities, num_of_nodes):

    i = 0
    labels = list(range(num_of_nodes))
    for community in communities:
        for node in community:
            labels[node] = i
        i += 1
    
    return labels

# Gets Ground truth from data supplied by file
def get_ground_truth_labels_from_graph(G):

    ground_truths = []

    for node in G.nodes():
        ground_truths.append(G.node[node]['value'])
    
    return ground_truths

def apply_community_value_to_graph(G, labels):

    i = 0
    for node in G.nodes():
        G.node[node]['value'] = labels[i]
        i += 1
    
    return G

def print_scatter_plot(scatter_plot, xaxis='Degree', yaxis1='Probability of Degree', yaxis2='Probability of Degree', title='Degree Destribution:', message=''):

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(scatter_plot[0], scatter_plot[1], 'b-o')
    ax2.plot(scatter_plot[0], scatter_plot[2], 'r-o')

    ax1.grid(True)
    ax1.set_xlabel(xaxis)
    ax1.set_ylabel(yaxis1, color='b')
    ax2.set_ylabel(yaxis2, color='r')

    plt.title(title + message)
    
    plt.show()
    plt.close()

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
    
    average_nmi = round(mean(nmi_list), 4)
    average_ars = round(mean(ars_list), 4)
    
    print('Average NMI:', average_nmi)
    print('Average ARS:', average_ars)

    return average_nmi, average_ars

option = sys.argv[1]
file_name = sys.argv[2]
name = sys.argv[3]
method = sys.argv[4]

print('Assignment 3 - Node Classification\n')

if option == 'a':
    print('Real Data -', name)

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
    nmi_list = []
    ars_list = []

    for drop_factor in drop_factors:
        
        print('\nNode Prediction when', int(drop_factor*100), r'% of nodes are dropped')
        g = deepcopy(G)

        for node in random.sample(g.nodes(), int(number_of_nodes*drop_factor)):
            del g.node[node]['value']
        
        nmi, ars = calculate_node_classification_accuracy(g, 'value', labels_truth, method)
        
        nmi_list.append(nmi)
        ars_list.append(ars)
    
    print_scatter_plot([drop_factors, nmi_list, ars_list], 'Drop Factor', 'Average NMI', 'Average ARS', name + ' Node Classification')

    with open(name+'-'+method+'.csv', mode='w') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        file_writer.writerow(['DropFactor', 'NMI Score', 'ARS Score'])

        for i in range(len(drop_factors)):
            file_writer.writerow([drop_factors[i], nmi_list[i], ars_list[i]])
        
elif option == 'b':
    print('GCN Data - ', name, '\n')

    # Unpickle and load data
    with open(file_name + 'y', 'rb') as f:
        labelsy = pkl.load(f, encoding='latin1')
    with open(file_name + 'ty', 'rb') as f:
        labelsty = pkl.load(f, encoding='latin1')
    with open(file_name + 'ally', 'rb') as f:
        labels = pkl.load(f, encoding='latin1')
    with open(file_name + 'graph', 'rb') as f:
        graph = pkl.load(f, encoding='latin1')
    
    num_of_groud_truths = len(labels)
    num_of_train = len(labelsy)
    num_of_test = len(labelsty)
    drop_factor = round((num_of_test/(num_of_train+num_of_test)), 4)
    print('Number of Ground Truth in Training:', num_of_train)
    print('Number of Ground Truth in Testing:', num_of_test)
    print('Number of Ground Truth in Total:', num_of_groud_truths)
    print('Drop Factor:', drop_factor)

    G = convert_to_networkx(labels, graph)
    labels_truth = get_ground_truth_labels_from_graph(G)
    number_of_nodes = nx.number_of_nodes(G)
    #print('Ground Truth Labels:\n', labels_truth)
    print('\nNumber of Nodes in Graph:', number_of_nodes)

    print('\nNode Prediction when', (drop_factor*100), r'% of nodes are dropped')

    for node in random.sample(G.nodes(), int(number_of_nodes*drop_factor)):
        del G.node[node]['value']
    
    nmi, ars = calculate_node_classification_accuracy(G, 'value', labels_truth, method)

    with open(name+'-'+method+'.csv', mode='w') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        file_writer.writerow(['DropFactor', 'NMI Score', 'ARS Score'])
        file_writer.writerow([drop_factor, nmi, ars])

elif option == 'c':
    print('Synthetic Data - No File')

    # Settings provided by the prof
    n = 1000
    tau1 = 3
    tau2 = 1.5
    mu_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    #mu_list = [0.5]
    average_degree = 5
    minimum_community=20

    drop_factor = 0.2

    nmi_list = []
    ars_list = []

    for mu in mu_list:

        print('\nNode Prediction when mu is', mu, r'and 20% of nodes are dropped')

        G = LFR_benchmark_graph(n, tau1, tau2, mu, average_degree, min_community=minimum_community)
        #print('First Node:',G.nodes[0])
        communities = {frozenset(G.nodes[v]['community']) for v in G}
        #print('Communities:\n', communities)
        #print('Number of Ground Turth Communities:', len(communities))
        labels_truth = get_labels_from_community(communities, n)
        #print('Ground Truth Labels:\n', labels_truth)
        G = apply_community_value_to_graph(G, labels_truth)
        #print('First Node Modified:',G.nodes[0])

        for node in random.sample(G.nodes(), int(n*drop_factor)):
            del G.node[node]['value']
        
        nmi, ars = calculate_node_classification_accuracy(G, 'value', labels_truth, method)

        nmi_list.append(nmi)
        ars_list.append(ars)
    
    print_scatter_plot([mu_list, nmi_list, ars_list], 'Mu', 'Average NMI', 'Average ARS', 'LFR Benchmark Graph Node Classification')

    with open(name+'-'+method+'.csv', mode='w') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        file_writer.writerow(['Mu', 'NMI Score', 'ARS Score'])

        for i in range(len(mu_list)):
            file_writer.writerow([mu_list[i], nmi_list[i], ars_list[i]])
