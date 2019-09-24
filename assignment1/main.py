from scipy.sparse import csc_matrix
import sys
import string

def import_network(filename):
    file = open(filename, 'r')

    row = []
    col = []
    data = []

    for line in file:
        vertex = line.split()
        row.append(int(vertex[0]))
        col.append(int(vertex[1]))
        data.append(1)
    
    file.close()

    number_of_nodes = max(max(row), max(col)) + 1

    return csc_matrix((data, (row, col)), shape=(number_of_nodes, number_of_nodes))

def degree_distribution(matrix, size):

    degrees = []

    for i in range(size):

        col = matrix.getcol(i)
        degrees.append(col.sum())
        print('Col', i, ':', col.sum(), '\n', col.toarray())

    return degrees




network_file = sys.argv[1]

sparse_matrix = import_network(network_file)

nodes = sparse_matrix.get_shape()[1]

print('Number of Nodes:', nodes)
print('Matrix: \n', sparse_matrix.toarray())

degrees = degree_distribution(sparse_matrix, nodes)

print(degrees)






