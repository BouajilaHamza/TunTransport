import scrapy


class SoretrasSpider(scrapy.Spider):
    name = "soretras"
    allowed_domains = ["soretras.com.tn"]
    start_urls = ["https://soretras.com.tn/tarif_reg3"]
    payload = {}
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '36e517a67a9e1ad4eee8bbbfe173c3ad=7511afbd6591ba48b3de986d08f9062bb705b2f4; 36e517a67a9e1ad4eee8bbbfe173c3ad=4cc1adb7ad8471b85279729be52ce271752f9bc7',
    'Referer': 'https://soretras.com.tn/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    def parse(self, response):
        departs = response.xpath('//select[@id="station"]/option')

        # for depart in departs :
        #     if depart.xpath('.//@value').get() != '0':
        #         yield {depart.xpath('.//text()').get(): depart.xpath('.//@value').get()}

        departs = {
            depart.xpath('.//text()').get(): depart.xpath('.//@value').get()
            for depart in departs if depart.xpath('.//@value').get() != '0'
        }
        self.logger.info(departs)
        depart_id = departs[self.depart]
        if depart_id == '1':
            depart_id = "a"
        elif depart_id == '2':
            depart_id = "v"
            
        url = f"https://soretras.com.tn/pages/abonnementstarifreg1/{depart_id}"
        payload = f"get_option={depart_id}"
        headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '36e517a67a9e1ad4eee8bbbfe173c3ad=7511afbd6591ba48b3de986d08f9062bb705b2f4; 36e517a67a9e1ad4eee8bbbfe173c3ad=7511afbd6591ba48b3de986d08f9062bb705b2f4',
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
        yield scrapy.Request(url , method='POST', headers=headers, body=payload, callback=self.parse_destinations)
    
    def parse_destinations(self, response):
        options = response.xpath("//option")

        values = {
        dest.xpath(".//text()").get(): dest.xpath(".//@value").get() for dest in options if dest.xpath(".//@value").get() != "0"
                }
        self.logger.info(values)
        search_key = values[self.destination]
        url = f"https://soretras.com.tn/pages/abonnementstarifreg2/{search_key}"
        payload = f"get_option={search_key}"
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
        yield scrapy.Request(url, method='POST', headers=headers, body=payload, callback=self.parse_tarifs)
    
    def parse_tarifs(self, response):
        all=[]
        table = response.xpath("//table/tr")

        for tr in table[2:]:
            yield {
                "company": "Soretras",
                "depart_time": tr.xpath(".//td[1]/text()").get(),
                "arrive_time": tr.xpath(".//td[2]/text()").get(),
                "price": tr.xpath(".//td[3]/text()").get(),
            }

        

