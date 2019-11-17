import sys
import urllib.request
import os.path

print('Data Collection Starting')

month = sys.argv[1]
begin_day = int(sys.argv[2]) # Shoud start at 1
end_day = int(sys.argv[3]) # Should finish at 32

url = 'https://data.gharchive.org/2018-01-01-0.json.gz'
store = '/Users/fozail/SchoolDev/comp596/project/data/2018-01-01-0.json.gz'

opener = urllib.request.URLopener()
# Add a header to throw off crawler protection on wesite
opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3')

for day in range(begin_day, end_day):
    for hour in range(0, 24):
        if day < 10:
            url = 'https://data.gharchive.org/2018-' + month + '-0' + str(day) + '-' + str(hour) + '.json.gz'
            store = '/Users/fozail/SchoolDev/comp596/project/data/2018-' + month + '-0' + str(day) + '-' + str(hour) + '.json.gz'
        else:
            url = 'https://data.gharchive.org/2018-' + month + '-' + str(day) + '-' + str(hour) + '.json.gz'
            store = '/Users/fozail/SchoolDev/comp596/project/data/2018-' + month + '-' + str(day) + '-' + str(hour) + '.json.gz'
        
        if os.path.isfile(store) == False:
            try:
                opener.retrieve(url, store)
            except Exception as e:
                print('Could not retreive data for URL:', url)
                print('Reason:', e)