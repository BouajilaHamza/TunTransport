from typing import Any
import scrapy
from scrapy.http import Response


class SrtgSpider(scrapy.Spider):
    name = "srtg"
    allowed_domains = ["www.srtgouafel.com.tn"]
    start_urls = ["https://api.srtgouafel.com.tn/api/stationinter"]
    all_dep_stations = []
    headers = {"Content-Type": "multipart/form-data"}
    
    def parse(self, response):
        if response.json()["status"]:
            for page in range(response.json()["total_pages"]):
                yield scrapy.Request(f"https://api.srtgouafel.com.tn/api/stationinter?page={page}", headers=self.headers,callback=self.fetch_all_depstations)

                     
    def fetch_all_depstations(self,response):
        self.all_dep_stations.extend(response.json()["stations"])
        
        
        
    def fetch_station_arr(self):
        for dep in self.all_dep_stations:
            if self.depart in dep["titre_ar"]:
                self.selecteddep = dep["id"]
                response = scrapy.Request(f"https://api.srtgouafel.com.tn/api/station_arr?arr={self.selecteddep}", headers=self.headers)
        
        
        
        if response.json()["status"]:
            for dest in response.json()["stations"]:
                if self.destination in dest["titre_ar"]:
                    self.selectedarr = dest["id"]
        else:
            self.stationsarr = {}

    def fetch_horaires(self):
        response = scrapy.Request(
            f"https://api.srtgouafel.com.tn/api/liste_by_station?st1={self.selecteddep}&st2={self.selectedarr}", headers=self.headers)
        if response.json()["status"]:
            for voy in response.json()["horaires"]:
                yield {
                    "company": "SRTG",
                    "depart_time": voy["depart"],
                    "arrive_time": voy["arr"],
                    "depart_station": voy['title_fr'].split(" - ")[0],
                    "arrive_station": voy['title_fr'].split(" - ")[1],
                }
           
        