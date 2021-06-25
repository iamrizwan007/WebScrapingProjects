# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest


class GunspiderSpider(scrapy.Spider):
    name = 'gunspider'
    # allowed_domains = ['palmettostatearmory.com']
    # start_urls = ['https://palmettostatearmory.com/guns.html']

    def start_requests(self):
        yield SeleniumRequest(
            url="https://palmettostatearmory.com/guns.html",
            wait_time=1,
            callback=self.parse,
            headers={
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'DNT': '1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
                'Sec-Fetch-User': '?1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'navigate',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
            }
        )

    def parse(self, response):
        items = response.xpath("//a[@class='product-item-link']")
        for item in items:
            yield {
                'Name': item.xpath(".//text()").get()
            }
