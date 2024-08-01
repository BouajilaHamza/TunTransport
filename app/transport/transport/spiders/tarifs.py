import scrapy


class TarifsSpider(scrapy.Spider):
    name = "tarifs"
    allowed_domains = ["sntri.com.tn",
                       "www.srtgouafel.com.tn",
                       "soretras.com.tn",
                       "srtm.tn"]
    headers = {"Content-Type": "multipart/form-data"}
    start_urls = ["https://soretras.com.tn/tarif_reg3",
                  "https://api.srtgouafel.com.tn/api/stationinter",
                  "https://srtm.tn/?lang=ar"
                ]
    def parse(self, response):
        pass
