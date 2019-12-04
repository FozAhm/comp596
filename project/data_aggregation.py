import sys
import time
import csv
import os

start_time = time.time()

print('Data Aggregation Script')

event_type = sys.argv[1] # Should be Edges or Nodes for aggregation
data_location = sys.argv[2] # Should be '/Users/fozail/SchoolDev/comp596/project/data/'
output_location = sys.argv[3] # Should be '/Users/fozail/SchoolDev/comp596/project/edges/all_edges.csv'

print('Looking for', event_type)

output_file = open(output_location, 'a')
output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

data_directory = os.fsencode(data_location)

all_objects = {}

for file in os.listdir(data_directory):
    filename = os.fsdecode(file)
    file_path = data_location + filename
    print('Looking through', filename, '...')

    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        if event_type == 'Nodes':
            for row in csv_reader:
                all_objects[row[0]] = row[1]
        elif event_type == 'Edges':
            for row in csv_reader:
                key = (row[0], row[1])
                if key in all_objects:
                    all_objects[key] = all_objects[key] + 1
                else:
                    all_objects[key] = 1

if event_type == 'Nodes':
    for key,value in all_objects.items():
        output_writer.writerow([key, value])
elif event_type == 'Edges':
    for key,value in all_objects.items():
        output_writer.writerow([key[0], key[1], value])

output_file.close()
