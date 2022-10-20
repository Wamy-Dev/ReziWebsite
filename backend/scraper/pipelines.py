import meilisearch

class MeiliPipeline:
    # client = meilisearch.Client('http://127.0.0.1:7700', 'masterKey')
    # index = client.index('games')
    def process_item(self, item, spider):
        data = dict(item)
        print(data)
        # self.index.add_documents(data)
        return item