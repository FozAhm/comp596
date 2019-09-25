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

def degree_distribution(degree_frequency, size):

    degree = []
    porbability = []

    for key, value in degree_frequency.items():
        degree.append(key)
        porbability.append(value/size)
    
    return [degree,porbability]

def print_scatter_plot(scatter_plot, xaxis='Degree', yaxis='Probability of Degree', title='Degree Destribution:',log=True):

    if log:
        fit = np.polyfit(np.log10(scatter_plot[0]), np.log10(scatter_plot[1]), 1)
    else:
        fit = np.polyfit(scatter_plot[0], scatter_plot[1], 1)

    best_fit = 'y = ' + str(np.round(fit[0], 6)) + 'x + ' + str(np.round(fit[1], 6)) 
    
    plt.plot(scatter_plot[0], scatter_plot[1], 'bo')
    
    if log:
        plt.yscale('log')
        plt.xscale('log')

    plt.title(title + '\n' + best_fit)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    
    plt.grid(True)
    
    plt.show()
    plt.close()

network_file = sys.argv[1]
undirected = str_to_bool(sys.argv[2])
option = sys.argv[3]

print('Loading Graph from file', network_file, '...')
sparse_matrix = import_network(network_file, undirected)
print('Done Loading')
#print('Matrix: \n', sparse_matrix.toarray())

nodes = sparse_matrix.get_shape()[1]
print('Number of Nodes in Graph:', nodes)

if(option == 'a'):
    
    degrees = matrix_degrees(sparse_matrix, nodes, undirected)
    #print('Degrees:\n', degrees)

    degree_frequency = list_frequency(degrees)
    #print(degree_frequency)

    degree_dist = degree_distribution(degree_frequency, nodes)
    print_scatter_plot(degree_dist)
elif(option == 'b'):
    
    A3 = sparse_matrix*sparse_matrix*sparse_matrix
    #print(A3.toarray())
    A3_diagonal = A3.diagonal()
    
else:
    print('Incorrect Option Selected...')





