import meilisearch
import requests
import json
import os
from datetime import datetime
import decouple
from decouple import config
#
SEARCHCLIENT = config('SEARCHCLIENT')
SEARCHAPIKEY = config('SEARCHAPIKEY')
CRONMONITORING = config("CRONMONITORING")
#
#client = meilisearch.Client('serverlocation', 'apikey')
client = meilisearch.Client(SEARCHCLIENT, SEARCHAPIKEY)
json_file = open('./components/outputsearchready.json')
games = json.load(json_file)
client.delete_index('games') #deletes previous index due to the way meilisearch does indexes, it adds on top of, and updating doesn't work very well, so a good ole delete and create works fine.
client.index('games').add_documents(games)
print('finished entire process.')
#
try:
	now=datetime.now()
	current_time = now.strftime("%H:%M:%S")
	requests.post(CRONMONITORING, data=f'Time finished: {current_time}.')
except requests.RequestException as e:
	print("Ping failed: %s" % e)