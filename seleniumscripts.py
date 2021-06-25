# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest


class SlickspiderSpider(scrapy.Spider):
    name = 'slickspider'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://slickdeals.net/computer-deals",
            wait_time=2,
            callback=self.parse
        )

    def parse(self, response):
        products = response.xpath("//li[@class='fpGridBox grid altDeal hasPrice']")
        for product in products:
            name = product.xpath(".//a[contains(@class,'itemTitle')]/text()").get()
            link = product.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']/@href").get()
            # yield {
            #     'Name': name,
            #     'User-Agent': response.request.headers['User-Agent']
            # }
            absolute = f"https://slickdeals.net{link}"
            yield SeleniumRequest(
                url=absolute,
                wait_time=2,
                callback=self.product_comment,
                meta={'Name': name}
            )

        # next_page = response.xpath("//a[@data-role='next-page']/@href").get()
        # if next_page:
        #     abs_url = f"https://slickdeals.net{next_page}"
        #     print(abs_url)
        #     print("***********************")
        #     yield SeleniumRequest(url=abs_url, wait_time=2, callback=self.parse, headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'})

    def product_comment(self, response):
        name = response.meta['Name']
        comments = response.xpath("//div[@id='commentsBox']//span/text()").get()
        yield {
            'Name': name,
            'Comment': comments
        }

        print('''
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .


        ''')