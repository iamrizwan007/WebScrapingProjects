# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector

class DuckspiderSpider(scrapy.Spider):
    name = 'duckspider'

    def start_requests(self):
        yield SeleniumRequest(
            url= "https://duckduckgo.com/",
            wait_time= 2,
            callback= self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        srch_btn = driver.find_element_by_xpath("//input[@id='search_form_input_homepage']")
        srch_btn.send_keys("Hello World")
        srch_btn.send_keys(Keys.ENTER)

        html = driver.page_source
        response_obj = Selector(text=html)

        links = response_obj.xpath("//a[@class='result__a js-result-title-link']")
        for link in links:
            url = link.xpath(".//@href").get()

            yield {
                'Link': url
            }
