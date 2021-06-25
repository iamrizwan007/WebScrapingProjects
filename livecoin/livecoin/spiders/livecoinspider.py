# -*- coding: utf-8 -*-
import time

import scrapy
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector

class LivecoinspiderSpider(scrapy.Spider):
    name = 'livecoinspider'
    allowed_domains = ['https://web.archive.org']
    start_urls = ['https://web.archive.org/web/20200116052415/https://www.livecoin.net/en']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        driver.set_window_size(1920,10000)
        driver.get("https://web.archive.org/web/20200116052415/https://www.livecoin.net/en")
        rur_tab = driver.find_elements(By.CLASS_NAME, "filterPanelItem___2z5Gb ")
        rur_tab[4].click()
        time.sleep(2)
        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        response = Selector(text=self.html)
        pairs = response.xpath("//div[@class='ReactVirtualized__Table__rowColumn tableRowColumn___rDsl0']/div")
        for pair in pairs:
            yield {
                'Pair':pair.xpath(".//text()").get()
            }

