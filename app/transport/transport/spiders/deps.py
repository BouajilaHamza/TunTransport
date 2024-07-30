from typing import Iterable
import scrapy


class DepsSpider(scrapy.Spider):
    name = "deps"
    allowed_domains = ["sntri.com.tn",
                       "www.srtgouafel.com.tn",
                       "soretras.com.tn",
                       "srtm.tn"]
    all_dep_stations = []
    headers = {"Content-Type": "multipart/form-data"}
    start_urls = ["https://soretras.com.tn/tarif_reg3",
                  "https://api.srtgouafel.com.tn/api/stationinter",
                  "https://srtm.tn/?lang=ar"
                ]
    def start_requests(self) :
        
        # for dep in self.all_dep_stations:
        #     if self.depart in dep["titre_ar"]:
        #         self.selecteddep = dep["id"]
        if self.Company == "SRTG":
            yield scrapy.Request(f"https://api.srtgouafel.com.tn/api/station_arr?arr={self.dep_id}", headers=self.headers,callback=self.parse_srtg)
        
        
    def parse_srtg(self, response):
        if response.json()["status"]:
            for dest in response.json()["stations"]:
                if dest["active"]:
                    yield {
                        "Depart": self.depart,
                        "Name": dest["titre_ar"],
                        "Id": dest["id"],
                        "Company": self.Company,
                        "MappedName":None
                    }
      
    def parse(self, response):
        pass
