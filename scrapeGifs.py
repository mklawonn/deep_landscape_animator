import json
import requests
import os

limit = 100
cutoff = 50000
api_key = "dc6zaTOxFJmzC"
imgURLs = []
i = 0

while True:
    if (i % 100) == 0:
        print "Getting page {0}".format(i)
    url = "http://api.giphy.com/v1/gifs/search?q=time+lapse+natural&limit={0}&offset={1}&api_key={2}".format(limit,i,api_key)
    r = requests.get(url)
    rjson = r.json()
    for gif in rjson['data']:
        try:
            imgURLs.append(gif['images']['downsized_small']['mp4'])
        except:
            continue
	
    count = int(rjson['pagination']['count'])
    if(count < limit):
        break

    if (i * limit) > 150000:
        break
    i += 1	

i = 0

for url in imgURLs:
    start = url.index("media/") + len("media/")
    stop = url.index("/", start)
    directory = "./data/{0}/".format(i/1000)
    local_filename = "{0}{1}".format(directory, url[start:stop])
    if (i % 1000) == 0:
        print "Downloading gif number {0}".format(i)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except:
                print "Making directory {0} failed".format(directory)
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    i += 1
