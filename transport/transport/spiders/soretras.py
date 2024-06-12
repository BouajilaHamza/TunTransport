import scrapy


class SoretrasSpider(scrapy.Spider):
    name = "soretras"
    allowed_domains = ["soretras.com.tn"]
    start_urls = ["https://soretras.com.tn"]

    def parse(self, response):
        pass
