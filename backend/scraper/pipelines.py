import os
class BasicPipeline:
    def open_spider(self, spider):
        os.remove('rezi.csv')
    def process_item(self, item, spider):
        data = dict(item)
        print(data)
        return item
        


