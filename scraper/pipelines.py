import requests
import time
import json
class BasicPipeline:
    def process_item(self, item, _):
        data = dict(item)
        # check if game link is broken
        with open("deadlinks.json", "r") as json_file:
            deadlinks = json.load(json_file)
        if data['link'] in deadlinks:
            return
        # get IGDB url
        igdb_url = 'https://igdb.com/search_autocomplete_all?q='
        try:
            igdb_data = requests.get(igdb_url + data['title'], headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
            }).json()
        except Exception:
            return data
        try:
            if len(igdb_data["game_suggest"]) >= 1:
                data['igdb_url'] = "https://igdb.com" + igdb_data["game_suggest"][0]['url']
            time.sleep(0.1) # 10 requests per second
        except Exception:
            pass
        return data
        


