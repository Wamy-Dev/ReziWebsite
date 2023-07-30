import requests
import time
class BasicPipeline:
    def process_item(self, item, _):
        data = dict(item)
        igdb_url = 'https://igdb.com/search_autocomplete_all?q='
        igdb_data = requests.get(igdb_url + data['title'], headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }).json()
        if len(igdb_data["game_suggest"]) >= 1:
            data['igdb_url'] = "https://igdb.com" + igdb_data["game_suggest"][0]['url']
        time.sleep(0.3333) # 3 requests per second
        return data
        


