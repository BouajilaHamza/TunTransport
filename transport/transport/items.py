# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SntriItem(scrapy.Item):
    Company = scrapy.Field()
    Depart = scrapy.Field()
    Destination = scrapy.Field()
    DepartTime = scrapy.Field()
    EstimatedArriveTime = scrapy.Field()
    Distance = scrapy.Field()
    Price = scrapy.Field()
    
