import meilisearch
import json
import os
import decouple
from decouple import config
#
SEARCHCLIENT = config('SEARCHCLIENT')
SEARCHAPIKEY = config('SEARCHAPIKEY')
#
#client = meilisearch.Client('serverlocation', 'apikey')
client = meilisearch.Client(SEARCHCLIENT, SEARCHAPIKEY)
json_file = open('./components/outputsearchready.json')
games = json.load(json_file)
client.delete_index('games') #deletes previous index due to the way meilisearch does indexes, it adds on top of, and updating doesn't work very well, so a good ole delete and create works fine.
client.index('games').add_documents(games)
print('finished entire process.')