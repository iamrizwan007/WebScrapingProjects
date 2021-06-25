# -*- coding: utf-8 -*-
import scrapy


class FinancespiderSpider(scrapy.Spider):
    name = 'financespider'
    allowed_domains = ['www.yellowpages.com.au']
    start_urls = ['https://www.yellowpages.com.au/search/listings?clue=financial+planners&locationClue=&lat=&lon=']

    def parse(self, response):
        items = response.xpath("//div[@class='search-contact-card call-to-actions-4 feedback-feature-on']")
        for item in items:
            email = item.xpath(".//a[contains(@href,'mailto')]/@data-email").get()
            business = item.xpath(".//a[@class='listing-name']/text()").get()
            yield {
                'Business Name':business,
                'Email': email,
                'User-Agent': response.request.headers['User-Agent']
            }

        next_page = response.xpath("//a[text()='Next »']/@href").get()
        if next_page:
            print("**********************",next_page)
            next_abs_url = response.urljoin(next_page)
            print("****", next_abs_url)
            yield response.follow(
                url= next_abs_url,
                callback= self.parse,
                headers= {
                    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
                }
            )


