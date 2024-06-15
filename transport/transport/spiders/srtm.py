import scrapy


class SrtmSpider(scrapy.Spider):
    name = "srtm"
    allowed_domains = ["srtm.tn"]
    start_urls = ["https://srtm.tn"]

    def parse(self, response):
        agences = response.xpath('//*[@id="nav"]/li[3]/ul/li')
        for agence in agences :
            url = agence.xpath('a/@href').get()
            name = agence.xpath('a/text()').get()
            if name.lower() in ['agence houmt souk',"agence midoun"] :
                name = "Djerba"
            self.logger.info(f"{name.lower()}\t{self.depart.lower()}\t{self.depart.lower() in name.lower()}")
            if self.depart.lower() in name.lower():
                print(url)
                yield scrapy.Request(url, callback=self.parse_agence, meta={"name":name})
                break
    
    
    def parse_agence(self, response):
        
        table = response.xpath('//*[contains(@id, "tablepress")]')
        agency_names = table.xpath('./thead/tr/th/text()').getall()
        rows = table.xpath('./tbody/tr')
        for idx,agency in enumerate(agency_names):
            for row in rows:
                hour = row.xpath(f'./td[{idx}]/text()').get()
                
                self.logger.info(f"{agency.lower()}\t{self.destination.lower()}\t{self.destination.lower() in agency.lower()}")
                if hour != None and self.destination.lower() in agency.lower():
                    yield {
                        "company":"SRTM",
                        "depart":response.meta["name"],
                        "destination":agency.replace('Agence',"").strip(),
                        "depart_time":hour ,
                        "arrive_time":None,
                        "price":None
                    }
        
            