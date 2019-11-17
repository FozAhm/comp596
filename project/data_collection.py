import sys
import urllib.request

print('Data Collection Starting')

month = sys.argv[1]

url = 'https://data.gharchive.org/2018-01-01-0.json.gz'
store = '/Users/fozail/SchoolDev/comp596/project/data/2018-01-01-0.json.gz'

opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3')

for day in range(1, 32):
    for hour in range(0, 24):
        if day < 10:
            url = 'https://data.gharchive.org/2018-' + month + '-0' + str(day) + '-' + str(hour) + '.json.gz'
            store = '/Users/fozail/SchoolDev/comp596/project/data/2018-' + month + '-0' + str(day) + '-' + str(hour) + '.json.gz'
        else:
            url = 'https://data.gharchive.org/2018-' + month + '-' + str(day) + '-' + str(hour) + '.json.gz'
            store = '/Users/fozail/SchoolDev/comp596/project/data/2018-' + month + '-' + str(day) + '-' + str(hour) + '.json.gz'

        try:
            opener.retrieve(url, store)
        except Exception as e:
            print('Could not retreive data for URL:', url)
            print('Reason:', e)