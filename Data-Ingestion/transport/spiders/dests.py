import scrapy


class DepsSpider(scrapy.Spider):
    name = "dests"
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
        # for dep in self.all_dep_stations:
        #     if self.depart in dep["titre_ar"]:
        #         self.selecteddep = dep["id"]
        self.logger.info(f"Depart: {self.depart},{self.dep_id} ,{self.Company}")
        if self.Company == "SRTG":
            yield scrapy.Request(
                f"https://api.srtgouafel.com.tn/api/station_arr?arr={self.dep_id}",
                headers=self.headers,
                callback=self.parse_srtg,
            )
        if self.Company == "SRTM":
            yield scrapy.Request(self.dep_id, callback=self.parse_srtm)
        if self.Company == "Soretras":
            url = f"https://soretras.com.tn/pages/Abonnementstarifreg1/{self.dep_id}"
            payload = f"get_option={self.dep_id}"
            headers = {
                "Accept": "*/*",
                "Accept-Language": "en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": "36e517a67a9e1ad4eee8bbbfe173c3ad=7511afbd6591ba48b3de986d08f9062bb705b2f4; 36e517a67a9e1ad4eee8bbbfe173c3ad=7511afbd6591ba48b3de986d08f9062bb705b2f4",
                "Origin": "https://soretras.com.tn",
                "Referer": "https://soretras.com.tn/tarif_reg3",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
            }
            yield scrapy.Request(
                url,
                method="POST",
                headers=headers,
                body=payload,
                callback=self.parse_soretras,
            )

    def parse_srtg(self, response):
        if response.json()["status"]:
            for dest in response.json()["stations"]:
                if dest["active"]:
                    yield {
                        "Depart": self.depart,
                        "Name": dest["titre_ar"],
                        "Id": dest["id"],
                        "Company": self.Company,
                        "MappedName": None,
                    }

    def parse_srtm(self, response):
        table = response.xpath('//*[contains(@id, "tablepress")]')
        agency_names = table.xpath("./thead/tr/th/text()").getall()
        for agency in agency_names:
            yield {
                "Depart": self.depart,
                "Name": agency,
                "Id": None,
                "Company": self.Company,
                "MappedName": None,
            }

    def parse_soretras(self, response):
        options = response.xpath("//option")
        for dest in options:
            if dest.xpath(".//@value").get() != "0":
                yield {
                    "Depart": self.depart,
                    "Name": dest.xpath(".//text()").get(),
                    "Id": dest.xpath(".//@value").get(),
                    "Company": self.Company,
                    "MappedName": None,
                }
