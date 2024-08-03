import json
import scrapy


class TarifsSpider(scrapy.Spider):
    name = "tarifs"
    allowed_domains = ["sntri.com.tn",
                       "www.srtgouafel.com.tn",
                       "soretras.com.tn",
                       "srtm.tn"]
    headers = {"Content-Type": "multipart/form-data"}
    
    def start_requests(self) :
        self.depart = json.loads(self.depart)   
        self.destination = json.loads(self.destination)
        if self.Company == "SRTG":
            yield scrapy.Request(f"https://api.srtgouafel.com.tn/api/station_arr?arr={self.destination['Id']}", headers=self.headers,callback=self.parse_srtg)
        if self.Company == "SRTM":
            yield scrapy.Request(self.destination['Id'],callback=self.parse_srtm)
            
        if self.Company == "Soretras":
          url = f"https://soretras.com.tn/pages/abonnementstarifreg2/{self.destination['Id']}"
          payload = f"get_option={self.destination['Id']}"
          headers = {
          'Accept': '*/*',
          'Accept-Language': 'en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6',
          'Connection': 'keep-alive',
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Origin': 'https://soretras.com.tn',
          'Referer': 'https://soretras.com.tn/tarif_reg3',
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-origin',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
          'X-Requested-With': 'XMLHttpRequest',
          'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"'
          }
          yield scrapy.Request(url, method='POST', headers=headers, body=payload, callback=self.parse_soretras)
    
    def parse_soretras(self, response):
        table = response.xpath("//table/tr")

        for tr in table[2:]:
            yield {
                "company": "Soretras",
                "depart_time": tr.xpath(".//td[1]/text()").get(),
                "arrive_time": tr.xpath(".//td[2]/text()").get(),
                "price": tr.xpath(".//td[3]/text()").get(),
                "depart": self.depart["Name"],
                "destination": self.destination["Name"]
            }

    
    def parse_srtg(self, response):
      pass 
    
    
    
    def parse_srtm(self, response):
      pass
    
    
    
    