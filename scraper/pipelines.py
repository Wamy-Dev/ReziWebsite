import requests
import time
import json
import os
class BasicPipeline:

    @staticmethod
    def ensure_file_exists(filename, initial_content):
        if not os.path.exists(filename):
            with open(filename, "w") as file:
                json.dump(initial_content, file)


    def process_item(self, item, _):
        data = dict(item)
        # Ensure deadlinks.json exists
        self.ensure_file_exists("deadlinks.json", [])

        with open("deadlinks.json", "r") as json_file:
            deadlinks = json.load(json_file)
            if data['link'] in deadlinks:
                return

        # Ensure igdb_cached.json exists
        self.ensure_file_exists("igdb_cached.json", {})

        with open("igdb_cached.json", "r") as json_file:
            try:
                igdb_cached = json.load(json_file)
            except Exception:
                igdb_cached = {}

        # get IGDB url
        if data['title'] in igdb_cached:
            data['igdb_url'] = igdb_cached[data['title']]
        else:
            igdb_url = 'https://igdb.com/search_autocomplete_all?q='
            try:
                igdb_data = requests.get(igdb_url + data['title'], headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                }).json()
            except Exception:
                data['igdb_url'] = None
                return data
            try:
                if len(igdb_data["game_suggest"]) >= 1:
                    data['igdb_url'] = "https://igdb.com" + igdb_data["game_suggest"][0]['url']
                    igdb_cached[data['title']] = data['igdb_url']
                    with open("igdb_cached.json", "w") as json_file:  # open with 'w' to overwrite
                        json.dump(igdb_cached, json_file)
                    time.sleep(1)  # 1 request per second
            except Exception:
                data['igdb_url'] = None
        return data
        


