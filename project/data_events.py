import json
import sys

file_path1 = sys.argv[1]
file_path2 = sys.argv[2]

event_types1 = {'ForkEvent', 'PushEvent', 'WatchEvent'}
event_types2 = {'ForkEvent', 'PushEvent', 'WatchEvent'}

with open(file_path1) as f:
    for line in f:
        event = json.loads(line)
        event_types1.add(event['type'])

with open(file_path2) as f:
    for line in f:
        event = json.loads(line)
        event_types2.add(event['type'])

print(event_types1.difference(event_types2))
print(event_types2.difference(event_types1))

