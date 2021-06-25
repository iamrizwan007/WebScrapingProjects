# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FinancialspiderSpider(CrawlSpider):
    name = 'financialspider'
    allowed_domains = ['www.yellowpages.com.au']
    start_urls = ['https://www.yellowpages.com.au/search/listings?clue=financial+planners&locationClue=&lat=&lon=']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[text()='Next »']"), callback= 'parse_item', follow=True),
    )

    def parse_item(self, response):
        items = response.xpath("//div[@class='search-contact-card call-to-actions-4 feedback-feature-on']")
        for item in items:
            email = item.xpath(".//a[contains(@href,'mailto')]/@data-email").get()

            yield {'Email': email}
