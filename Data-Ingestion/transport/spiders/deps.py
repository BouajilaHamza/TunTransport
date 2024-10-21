import scrapy


class DestsSpider(scrapy.Spider):
    name = "deps"
    allowed_domains = [
        "sntri.com.tn",
        "www.srtgouafel.com.tn",
        "soretras.com.tn",
        "srtm.tn",
    ]
    all_dep_stations = []
    headers = {"Content-Type": "multipart/form-data"}
    start_urls = [
        "https://soretras.com.tn/tarif_reg3",
        "https://api.srtgouafel.com.tn/api/stationinter",
        "https://srtm.tn/?lang=ar",
    ]

    def start_requests(self):
        for url in self.start_urls:
            if "soretras" in url:
                yield scrapy.Request(url, callback=self.parse_soretras)
            elif "srtgouafel" in url:
                yield scrapy.Request(
                    url, callback=self.parse_srtgouafel, headers=self.headers
                )
            elif "srtm" in url:
                yield scrapy.Request(url, callback=self.parse_srtm)

    def parse_soretras(self, response):
        departs = response.xpath('//select[@id="station"]/option')
        departs = {
            depart.xpath(".//text()").get(): depart.xpath(".//@value").get()
            for depart in departs
            if depart.xpath(".//@value").get() != "0"
        }

        for k, v in departs.items():
            if v == "1":
                v = "a"
            elif v == "2":
                v = "v"

            yield {"Name": k, "Id": v, "Company": "Soretras", "MappedName": None}

    def parse_srtgouafel(self, response):
        self.all_dep_stations.extend(response.json()["stations"])
        for dep in self.all_dep_stations:
            if dep["active"] == 1:
                yield {
                    "Name": dep["titre_fr"],
                    "Id": dep["id"],
                    "Company": "SRTG",
                    "MappedName": None,
                }

    def parse_srtm(self, response):
        agences = response.xpath('//*[@id="nav"]/li[3]/ul/li')
        for agence in agences:
            url = agence.xpath("a/@href").get()
            name = agence.xpath("a/text()").get()
            if name.lower() in ["agence houmt souk", "agence midoun"]:
                name = "Djerba"
            # self.logger.info(f"{name.lower()}\t{self.depart.lower()}\t{self.depart.lower() in name.lower()}")
            # if self.depart.lower() in name.lower():
            #     print(url)
            #     yield scrapy.Request(url, callback=self.parse_agence, meta={"name":name})
            #     break

            yield {"Name": name, "Id": url, "Company": "SRTM", "MappedName": None}
