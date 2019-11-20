import gzip
import json
import sys
import time
import csv

start_time = time.time()

print('Data Analysis Script')

month = sys.argv[1]
begin_day = int(sys.argv[2]) # Shoud start at 1
end_day = int(sys.argv[3]) # Should finish at 32, 31 or 29
event_type = sys.argv[4] # Should be ForkEvent or PushEvent or WatchEvent
data_location = sys.argv[5] # Should be '/Users/fozail/SchoolDev/comp596/project/data/'
output_location = sys.argv[6] # Should be '/Users/fozail/SchoolDev/comp596/project/edges/'

print('Looking for edges representing', event_type)

event_file_path = output_location + event_type+ 's-2018-' + month + '-' + str(begin_day) + '-' + str(end_day) + '.csv'

ignore_files = {
    data_location + '2018-10-21-23.json.gz',
    data_location + '2018-10-22-0.json.gz',
    data_location + '2018-10-22-1.json.gz'
}

EventCount = 0
num_of_files = 0

event_file = open(event_file_path, 'a')
event_writer = csv.writer(event_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

for day in range(begin_day, end_day):
    print('Searching for', event_type, 'edges on day', day, 'of month', month)
    for hour in range(0, 24):
        if day < 10:
            file_path = data_location + '2018-' + month + '-0' + str(day) + '-' + str(hour) + '.json.gz'
        else:
            file_path = data_location + '2018-' + month + '-' + str(day) + '-' + str(hour) + '.json.gz'
        
        if month == '10':
            if file_path in ignore_files:
                continue

        num_of_files += 1

        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            for line in f:
                event = json.loads(line)
                if event['type'] == event_type:
                    EventCount += 1
                    if event_type == 'ForkEvent':
                        event_writer.writerow([event['repo']['name'], event['payload']['forkee']['full_name']])
                    elif event_type == 'PushEvent':
                        event_writer.writerow([event['actor']['login'], event['repo']['name']])
                    elif event_type == 'WatchEvent':
                        event_writer.writerow([event['actor']['login'], event['repo']['name']])

print('Number of Files Scanned:', num_of_files)
print('Number of', event_type,':', EventCount)

event_file.close()

print("--- %s seconds ---" % (time.time() - start_time))