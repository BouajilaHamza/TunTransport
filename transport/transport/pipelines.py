# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class TransportPipeline:
    def process_item(self, item, spider):
        item["Depart"] = item["Depart"].replace("%20", " ")
        item["Destination"] = item["Destination"].replace("%20", " ")
        item['Price'] = re.sub(r'[^\d.]', '', item['Price'])
        return item
