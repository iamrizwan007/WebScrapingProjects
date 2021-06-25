# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GunspiderSpider(CrawlSpider):
    name = 'gunspider'
    allowed_domains = ['palmettostatearmory.com']
    # start_urls = ['https://palmettostatearmory.com/guns.html']

    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(url="https://palmettostatearmory.com/guns.html", headers={
            'User-Agent': self.agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='product-item-link"), callback='parse_item', follow=True,
             process_request='set_user_agent'),
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.agent
        return request

    def parse_item(self, response):
        sku = response.xpath("(//td)[1]/text()").get()
        yield {
            'SKU': sku
        }
