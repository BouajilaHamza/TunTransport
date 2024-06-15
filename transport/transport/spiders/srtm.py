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
            print(url)
            yield scrapy.Request(url, callback=self.parse_agence, meta={"name":name})
    
    
    def parse_agence(self, response):
        
        table = response.xpath('//*[contains(@id, "tablepress")]')
        agency_names = table.xpath('./thead/tr/th/text()').getall()
        rows = table.xpath('./tbody/tr')
        for idx,agency in enumerate(agency_names):
            for row in rows:
                hour = row.xpath(f'./td[{idx}]/text()').get()
                yield {
                    "depart":response.meta["name"],
                    "destination":agency,
                    "hour":hour 
                }
        
            