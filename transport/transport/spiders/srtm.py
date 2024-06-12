import scrapy


class SrtmSpider(scrapy.Spider):
    name = "srtm"
    allowed_domains = ["srtm.tn"]
    start_urls = ["https://srtm.tn"]

    def parse(self, response):
        pass
