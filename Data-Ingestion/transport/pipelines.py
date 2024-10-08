# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from pymongo import MongoClient

class SNTRItPipeline:
    def process_item(self, item, spider):
        item["Depart"] = item["Depart"].replace("%20", " ")
        item["Destination"] = item["Destination"].replace("%20", " ")
        item['Price'] = re.sub(r'[^\d.]', '', item['Price'])
        return item

class SoretrasPipeline:
    def process_item(self, item, spider):
        item['Price'] = re.sub(r'[^\d.]', '', item['Price'])
        return item

class SRTMPipeline:
    def process_item(self, item, spider):
        item['Price'] = re.sub(r'[^\d.]', '', item['Price'])
        return item
    

class MongoDBPipeline:
    def open_spider(self, spider):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['Transport']
        self.collection = self.db["Places"]
        self.tarif_collection = self.db['Tarif']
        self.deps_collection = self.db['Destinations']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # if spider.name == "soretras":
        #     self.tarif_soretras.insert_one(ItemAdapter(item).asdict())
        # elif spider.name == "srtm":
        #     self.tarif_srtm.insert_one(ItemAdapter(item).asdict())
        # elif spider.name == "srtg":
        if spider.name == "dests":
            self.collection.insert_one(ItemAdapter(item).asdict())
        elif spider.name == "deps":
            self.deps_collection.insert_one(ItemAdapter(item).asdict())
        else:
            self.tarif_collection.insert_one(ItemAdapter(item).asdict())
        # self.collection.insert_one(ItemAdapter(item).asdict())
        return item
