from scipy.sparse import csc_matrix
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

def matrix_degrees(matrix, size):

    degrees = []

    for i in range(size):

        col = matrix.getcol(i)
        degrees.append(col.sum())
        #print('Col', i, ':', col.sum(), '\n', col.toarray())

    return degrees

def degree_distribution(degree_frequency, size):

    degree = []
    porbability = []

    for key, value in degree_frequency.items():
        degree.append(key)
        porbability.append(value/size)
    
    return [degree,porbability]



network_file = sys.argv[1]
undirected = str_to_bool(sys.argv[2])

sparse_matrix = import_network(network_file, undirected)

nodes = sparse_matrix.get_shape()[1]

print('Number of Nodes:', nodes)
#print('Matrix: \n', sparse_matrix.toarray())

degrees = matrix_degrees(sparse_matrix, nodes)

#print(degrees)

degree_frequency = list_frequency(degrees)

#print(degree_frequency)

degree_dist = degree_distribution(degree_frequency, nodes)

print(degree_dist[1])





