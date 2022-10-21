class BasicPipeline:
    def process_item(self, item, spider):
        data = dict(item)
        print(data)
        return item
        


