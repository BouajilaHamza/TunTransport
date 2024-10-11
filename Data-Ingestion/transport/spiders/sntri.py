import scrapy
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from transport.items import SntriItem


class SntriSpider(scrapy.Spider):
    name = "sntri"
    allowed_domains = ["sntri.com.tn"]
    start_urls = ["https://sntri.com.tn"]
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    # options.add_argument('--headless')

    def parse(self, response):
        item = SntriItem()
        driver = Edge(options=self.options)
        driver.get(
            f"https://sntri.com.tn/search?from={self.depart}&to={self.destination}"
        )
        if "tftable" in driver.page_source:
            table = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tftable"))
            )
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                tds = row.find_elements(By.TAG_NAME, "td")
                if len(tds) != 0:
                    tds = [td.text for td in tds]
                    self.logger.info(tds)
                    item["Company"] = "SNTRI"
                    item["Depart"] = self.depart
                    item["Destination"] = self.destination
                    item["DepartTime"] = tds[2]
                    item["EstimatedArriveTime"] = tds[3]
                    item["Distance"] = tds[-2]
                    item["Price"] = tds[-1]
                    yield item

    # def get_schedules(self, response):
    #     self.logger.info(response)
    #     item = SntriItem()
    #     rows = response.xpath('//*[@id="app"]/div/main/div/div[3]/div/div[3]/table/tbody/tr')
    #     for row in rows:
    #         depart_time = row.xpath('td[3]/text()').get()
    #         estimated_arrive_time = row.xpath('td[4]/text()').get()
    #         distnace = row.xpath('td[4]/text()').get()
    #         price = row.xpath('td[5]/text()').get()
    #         item["Company"] = "SNTRI"
    #         item["Depart"] = response.meta["depart"]
    #         item["Destination"] = response.meta["destination"]
    #         item["DepartTime"] = depart_time
    #         item["EstimatedArriveTime"] = estimated_arrive_time
    #         item["Distance"] = distnace
    #         item["Price"] = price
    #         yield item
