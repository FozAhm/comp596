from scipy.sparse import csc_matrix
from scipy.sparse import csr_matrix
from scipy.sparse import csgraph
from scipy.sparse.csgraph import shortest_path
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import eigs
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import string

#TO USE
# First arguemnt should be path ot graph file
# Second Argument should be weather thisthe supplied graph is undirected or not by 'True' or 'False'
# Third Argument corresponds to what you want to calculate based on the assignment (a-g)

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

def list_frequency(list, input_dict= {}):

    frequency_dict = input_dict

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

    if undirected:

        for line in file:
            vertex = line.split()
            
            row.append(int(vertex[0]))
            col.append(int(vertex[1]))
            data.append(1)

            if((vertex[1] != vertex[0])):
                row.append(int(vertex[1]))
                col.append(int(vertex[0]))
                data.append(1)
    else:

        for line in file:
            vertex = line.split()
            row.append(int(vertex[0]))
            col.append(int(vertex[1]))
            data.append(1)
    
    file.close()

    number_of_nodes = max(max(row), max(col)) + 1

    return csc_matrix((data, (row, col)), shape=(number_of_nodes, number_of_nodes))

def matrix_degrees(matrix, size, undirected=True):

    degrees = []

    if(undirected == True):
        for i in range(size):

            col = matrix.getcol(i)
            degrees.append(col.sum())
            #print('Col', i, ':', col.sum(), '\n', col.toarray())
    elif (undirected == False):

        for i in range(size):

            col = matrix.getcol(i)
            row = matrix.getrow(i)
            degrees.append(col.sum() + row.sum())

    return degrees

def probability_distribution(frequency, size):

    degree = []
    porbability = []

    for key, value in frequency.items():
        #print('Key:', key, 'Value:', value, 'Size:', size)
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

        if ((A3_diagonal[i] == 0) or ((degree-1) < 1)):
            clustering.append(0)
        else:
            clustering.append(A3_diagonal[i]/(degree*(degree-1)))
    
    return clustering

def list_average(lst):
    
    list_sum = sum(lst)
    list_length = len(lst)
    list_average = list_sum/list_length

    return list_average

def gcc_percentage(labels_frequency, number_of_nodes):

    highest_key = 0
    highest_value = 0

    for key, value in labels_frequency.items():
        
        if value > highest_value:

            highest_value = value
            highest_key = key
    
    print('Number of Nodes in the GCC:', highest_value)
    print('Component Number:', highest_key)
    
    return ((highest_value/number_of_nodes)*100)

def degree_list(filename):
    file = open(filename, 'r')

    v1 = []
    v2 = []
    lines = 0

    for line in file:
        vertex = line.split()
        lines += 1
        
        v1.append(int(vertex[0]))
        v2.append(int(vertex[1]))

    file.close()

    return [v1, v2], lines

def degree_correlation(degree_lst, lines, degrees):

    #print(degree_lst, lines, degrees)

    d1 = []
    d2 = []

    for i in range(lines):
        d1.append(degrees[degree_lst[0][i]])
        d2.append(degrees[degree_lst[1][i]])

    return [d1, d2]

def spectral_gap(eigen_values):
    
    max_val = 0
    min_val = 100

    for value in eigen_values:

        if value > max_val:
            max_val = value
        if ((value > 0) and (value < min_val)):
            min_val = value
    
    return max_val-min_val

network_file = sys.argv[1]
file_name = network_file.split('/')
file_name_split = file_name[1].split('.')
name = file_name_split[0].capitalize()
#print('Name:', name)
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
    print_scatter_plot(degree_dist, title=name + ' Degree Destribution:')
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
    print_scatter_plot(clustering_dist, xaxis='Clustering Coeffecient', yaxis='Probability of Clustering Coeffecient', title=name + ' Clustering Coeffecient Distribution', log=True, logx=False, tofit=False, message='\nClustering Coeffecient Average: ' + str(np.round(clustering_average, 6)))
elif (option == 'c'):

    min_dist_matrix = shortest_path(csgraph=sparse_matrix, method='auto', directed = not undirected, return_predecessors=False, unweighted=True)
    #print('Minimum Distance Matrix:\n', min_dist_matrix)

    min_dist_frequency = {}

    for i in range(number_of_nodes):
        min_dist_frequency = list_frequency(min_dist_matrix[i], min_dist_frequency)
    #print('Minimum Distance Frequency:\n', min_dist_frequency)
    
    number_min_dist_val = number_of_nodes*number_of_nodes
    #print('Number of Minimum Distance Values:', number_min_dist_val)

    if float('Inf') in min_dist_frequency:
        infinity_number = min_dist_frequency.pop(float('Inf'))
        number_min_dist_val = number_min_dist_val - infinity_number 

    #print('Number of Minimum Distance Values:', number_min_dist_val)
    #print('Minimum Distance Frequency:\n', min_dist_frequency)

    # Calculate Average
    min_dist_average = 0

    for key, value in min_dist_frequency.items():
        min_dist_average += (key * value)
    
    min_dist_average = min_dist_average/number_min_dist_val

    min_dist_dist = probability_distribution(min_dist_frequency, number_min_dist_val)
    #print('Minimum Distance Distribution: \n', min_dist_dist)
    print_scatter_plot(min_dist_dist, xaxis='Minimum Distance', yaxis='Probability of Minimum Distance', title=name + ' Minimum Distance Distribution', log=False, logx=False, tofit=False, message='\nMinimum Distance Average: ' + str(np.round(min_dist_average, 6)))
elif(option == 'd'):

    file = open(str.lower(name)+'-d.txt', 'w')

    number_of_components, labels = connected_components(csgraph=sparse_matrix, directed= not undirected)
    print('Number of Connected Components:', number_of_components)
    file.write('Number of Connected Components:' + str(number_of_components)+ '\n')

    component_frequency = list_frequency(labels)
    #print('Component Frequency: \n', component_frequency)
    gcc_percent = gcc_percentage(component_frequency, number_of_nodes)

    print('Percentage of Nodes in the Greatest Connected Component:', np.round(gcc_percent, 2), '%')
    file.write('Percentage of Nodes in the Greatest Connected Component:' + str(np.round(gcc_percent, 2)) + '%')
    file.close()
elif(option == 'e'):
    laplace_matrix = csgraph.laplacian(sparse_matrix, normed=False)
    eigen_values, eigen_vectors = eigs(laplace_matrix.asfptype(), number_of_nodes-2)
    eigen_values = np.absolute(eigen_values)
    eigen_values = np.round(eigen_values, 2)
    number_of_eigen_values = len(eigen_values)
    #print('Eigen Values:\n', eigen_values)

    spectral_gap_val = spectral_gap(eigen_values)

    eigen_values_frequency = list_frequency(eigen_values)
    #print('Eigen Value Frequencies:\n', eigen_values_frequency)

    eigen_dist = probability_distribution(eigen_values_frequency, number_of_eigen_values)
    print_scatter_plot(eigen_dist, xaxis='Eigen Value', yaxis='Probability of Eigen Value', title=name + ' Eigen Value Distribution', log=True, logx=True, tofit=False, message='\nSpectral Gap: ' + str(spectral_gap_val))
elif(option == 'f'):

    degree_lst, lines = degree_list(network_file)
    #print('Degree List:\n', degree_lst)
    #print('Number of Lines:\n', lines)

    degree_correlations = degree_correlation(degree_lst, lines, degrees)
    #print('Degree Correlations:\n', degree_correlations)

    print_scatter_plot(degree_correlations, xaxis='di', yaxis='dj', title=name+' Degree Correlation', log=False, logx=False, tofit=False)
elif(option == 'g'):

    A3 = sparse_matrix*sparse_matrix*sparse_matrix
    #print('A3 Matrix: \n', A3.toarray())

    A3_diagonal = A3.diagonal()
    #print('A3 Diaganol: ', A3_diagonal)

    clustering_list = calculate_clustering(A3_diagonal, degrees, number_of_nodes)
    #print('Clustering: \n',clustering_list)

    print_scatter_plot([degrees, clustering_list], xaxis='degree i', yaxis='clustering coeffecient i', title=name + ' Degree vs Clustering Coeffecient', log=False, logx=False, tofit=False)
else:
    print('Incorrect Option Selected...')





