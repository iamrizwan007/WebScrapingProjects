# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest

class GunSpider(scrapy.Spider):
    name = 'gun'
    # allowed_domains = ['https://palmettostatearmory.com']
    # start_urls = ['http://as.com/']

    def start_requests(self):
        yield SeleniumRequest(
            url="https://palmettostatearmory.com/guns.html",
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        products = response.xpath("//a[@class='product-item-link']")
        for prod in products:
            link = prod.xpath(".//@href").get()
            yield {
                'Link': link
            }
