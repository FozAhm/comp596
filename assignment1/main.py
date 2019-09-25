from scipy.sparse import csc_matrix
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import string

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

def list_frequency(list):

    frequency_dict = {}

    for degree in list:

        if frequency_dict.get(degree):
            frequency_dict[degree] += 1
        else:
            frequency_dict[degree] = 1
    
    return frequency_dict

def import_network(filename, undirected):
    file = open(filename, 'r')

    row = []
    col = []
    data = []

    for line in file:
        vertex = line.split()
        row.append(int(vertex[0]))
        col.append(int(vertex[1]))
        data.append(1)

        if (undirected and (vertex[1] != vertex[0])):
            row.append(int(vertex[1]))
            col.append(int(vertex[0]))
            data.append(1)
    
    file.close()

    number_of_nodes = max(max(row), max(col)) + 1

    return csc_matrix((data, (row, col)), shape=(number_of_nodes, number_of_nodes))

def matrix_degrees(matrix, size, undirected=True):

    degrees = []

    for i in range(size):

        col = matrix.getcol(i)
        degrees.append(col.sum())
        #print('Col', i, ':', col.sum(), '\n', col.toarray())
    
    if (undirected == False):

        for i in range(size):

            row = matrix.getrow(i)
            degrees[i] += row.sum()

    return degrees

def probability_distribution(frequency, size):

    degree = []
    porbability = []

    for key, value in frequency.items():
        degree.append(key)
        porbability.append(value/size)
    
    return [degree,porbability]

def print_scatter_plot(scatter_plot, xaxis='Degree', yaxis='Probability of Degree', title='Degree Destribution:',log=True, logx=True, tofit=True, message=''):

    if tofit:
        if log:
            fit = np.polyfit(np.log10(scatter_plot[0]), np.log10(scatter_plot[1]), 1)
        else:
            fit = np.polyfit(scatter_plot[0], scatter_plot[1], 1)
        
        best_fit = '\ny = ' + str(np.round(fit[0], 6)) + 'x + ' + str(np.round(fit[1], 6)) 
    else:
        best_fit = ''

    plt.plot(scatter_plot[0], scatter_plot[1], 'bo')
    
    if log:
        plt.yscale('log')
    if logx:
        plt.xscale('log')

    plt.title(title + best_fit + message)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    
    plt.grid(True)
    
    plt.show()
    plt.close()

def calculate_clustering(A3_diagonal, degrees, size):

    clustering = []

    for i in range(size):

        degree = degrees[i]

        if (A3_diagonal[i] == 0):
            clustering.append(0)
        else:
            clustering.append(A3_diagonal[i]/(degree*(degree-1)))
    
    return clustering

def list_average(lst):
    
    list_sum = sum(lst)
    list_length = len(lst)
    list_average = list_sum/list_length

    return list_average

network_file = sys.argv[1]
undirected = str_to_bool(sys.argv[2])
option = sys.argv[3]

print('Loading Graph from file', network_file, '...')
sparse_matrix = import_network(network_file, undirected)
print('Done Loading')
#print('Matrix: \n', sparse_matrix.toarray())

number_of_nodes = sparse_matrix.get_shape()[1]
print('Number of Nodes in Graph:', number_of_nodes)

degrees = matrix_degrees(sparse_matrix, number_of_nodes, undirected)
#print('Degrees:\n', degrees)

if(option == 'a'):

    degree_frequency = list_frequency(degrees)
    #print('Degree Frequency: ', degree_frequency)

    degree_dist = probability_distribution(degree_frequency, number_of_nodes)
    print_scatter_plot(degree_dist)
elif(option == 'b'):
    
    A3 = sparse_matrix*sparse_matrix*sparse_matrix
    #print('A3 Matrix: \n', A3.toarray())

    A3_diagonal = A3.diagonal()
    #print('A3 Diaganol: ', A3_diagonal)

    clustering_list = calculate_clustering(A3_diagonal, degrees, number_of_nodes)
    #print('Clustering: \n',clustering_list)

    clustering_average = list_average(clustering_list)
    #print('Clustering Coeffecient Average: ', clustering_average)

    clustering_frequency = list_frequency(clustering_list)
    #print('Clustering Frequency: \n', clustering_frequency)

    clustering_dist = probability_distribution(clustering_frequency, number_of_nodes)
    print_scatter_plot(clustering_dist, xaxis='Clustering Coeffecient', yaxis='Probability of Clustering Coeffecient', title='Clustering Coeffecient Distribution', log=True, logx=False, tofit=False, message='\nClustering Coeffecient Average: ' + str(np.round(clustering_average, 6)))
    
else:
    print('Incorrect Option Selected...')





