import gzip
import json

data = []

with gzip.open('project/data/2018-01-01-0.json.gz', 'rt', encoding='utf-8') as f:
    for line in f:
        data.append(json.loads(line))

PullRequestEvent = 0
for event in data:
    if event['type'] == 'PullRequestEvent':
        PullRequestEvent += 1

print('Number of PullRequest Events:', PullRequestEvent)
