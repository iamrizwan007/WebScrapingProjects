# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AlabamaspiderSpider(CrawlSpider):
    name = 'alabamaspider'
    allowed_domains = ['www.buyandsellgoldsilver.com']

    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(
            url="http://www.buyandsellgoldsilver.com/Gold-Silver-Dealers/Alabama",
            headers={
                'User-Agent': self.agent
            }
        )

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='row'][2]/div/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//ul[@class='pagination']/li/a)[last()]"), callback='parse_item',follow=True,process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.agent
        return request

    def parse_item(self, response):
        cards = response.xpath("//div[@class='equal-height-content equal-height-box-custom single-row']")
        base = response.url
        for card in cards:
            jweller = card.xpath(".//h3/a/text()").get()
            address = card.xpath(".//span[@class='address']/text()").get()
            city = card.xpath(".//span[@class='city']/text()").get()
            statecode = card.xpath(".//span[@class='state_code']/text()").get()
            zip = card.xpath(".//span[@class='zip']/text()").get()
            phone = card.xpath(".//p/strong/text()").get()
            yield {
                'Jweller': jweller,
                'Address': address,
                'City': city,
                'StateCode': statecode,
                'Zip': zip,
                'Phone': phone,
                'URL' : base    # For my use, to verify the results
            }
