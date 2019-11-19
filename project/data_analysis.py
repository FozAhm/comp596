import gzip
import json
import sys
import time
import csv

start_time = time.time()

ForkEvent = 'ForkEvent'

month = sys.argv[1]
begin_day = int(sys.argv[2]) # Shoud start at 1
end_day = int(sys.argv[3]) # Should finish at 32, 31 or 29

fork_file_path = '/Users/fozail/SchoolDev/comp596/project/edges/ForkEvents-2018-' + month + '-' + str(begin_day) + '-' + str(end_day) + '.csv'

ForkEventCount = 0
num_of_files = 0

fork_file = open(fork_file_path, 'a')
fork_writer = csv.writer(fork_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

for day in range(begin_day, end_day):
    for hour in range(0, 24):
        if day < 10:
            file_path = '/Users/fozail/SchoolDev/comp596/project/data/2018-' + month + '-0' + str(day) + '-' + str(hour) + '.json.gz'
        else:
            file_path = '/Users/fozail/SchoolDev/comp596/project/data/2018-' + month + '-' + str(day) + '-' + str(hour) + '.json.gz'

        num_of_files += 1

        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            for line in f:
                event = json.loads(line)
                if event['type'] == ForkEvent:
                    ForkEventCount += 1
                    fork_writer.writerow([event['repo']['name'], event['payload']['forkee']['full_name']])

print('Number of Files Scanned:', num_of_files)
print('Number of Fork Events:', ForkEventCount)

fork_file.close()

print("--- %s seconds ---" % (time.time() - start_time))