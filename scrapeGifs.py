import json
import requests

limit = 100
api_key = "dc6zaTOxFJmzC"
imgURLs = []
i = 0

while True:
	url = "http://api.giphy.com/v1/gifs/search?q=time+lapse+natural&limit={0}&offset={1}&api_key={2}".format(limit,i,api_key)
	r = requests.get(url)
	rjson = r.json()
	for gif in rjson['data']:
		imgURLs.append(gif['images']['downsized_small']['mp4'])
	
	count = int(rjson['pagination']['count'])
	if(count < limit)
		break

	i += 1	
