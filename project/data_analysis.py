import gzip
import json
import sys
import time

start_time = time.time()

directory = 'project/data/'
filename = '2018-01-02-15.json.gz'

month = sys.argv[1]
begin_day = int(sys.argv[2]) # Shoud start at 1
end_day = int(sys.argv[3]) # Should finish at 32, 31 or 29

PullRequestEvent = 0
num_of_files = 0 

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
                if event['type'] == 'PullRequestEvent':
                    PullRequestEvent += 1

print('Number of Files Scanned:', num_of_files)
print('Number of PullRequest Events:', PullRequestEvent)

print("--- %s seconds ---" % (time.time() - start_time))