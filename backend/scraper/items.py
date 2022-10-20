import scrapy

class GameItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    id = scrapy.Field()