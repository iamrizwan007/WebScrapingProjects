# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest


class SlickspiderSpider(scrapy.Spider):
    name = 'slickspider'

    def start_requests(self):
        yield SeleniumRequest(
            url="http://www.buyandsellgoldsilver.com/Gold-Silver-Dealers",
            wait_time=10,
            callback=self.parse,
            headers={
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
            }
        )

    def parse(self, response):
        # products = response.xpath("//div[@class='row'][2]//a")
        # for link in products:
        #     name = link.xpath(".//text()").get()
        #     href = link.xpath(".//@href").get()
        for i in range(1, 3):
            name = response.xpath(f"(//div[@class='row'][2]//a)[{i}]/text()").get()
            href = response.xpath(f"(//div[@class='row'][2]//a)[{i}]/@href").get()
            yield SeleniumRequest(
                url=href,
                wait_time=10,
                callback=self.product_comment,
                meta={'Name': name},
                headers={
                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
                }
            )

    def product_comment(self, response):
        name = response.meta['Name']
        comments = response.xpath("//div[@class='equal-height-content equal-height-box-custom single-row']")
        for com in comments:
            jweller = com.xpath(".//h3/a/text()").get()
            address = com.xpath(".//span[@class='address']/text()").get()
            city = com.xpath(".//span[@class='city']/text()").get()
            statecode = com.xpath(".//span[@class='state_code']/text()").get()
            zip = com.xpath(".//span[@class='zip']/text()").get()
            phone = com.xpath(".//p/strong/text()").get()
            page_url = response.url
            yield {
                'Jweller': jweller,
                'Address': address,
                'City': city,
                'StateCode': statecode,
                'Zip': zip,
                'Phone': phone,
                'Base': name
            }
            # yield SeleniumRequest(
            #     url=page_url,
            #     wait_time=10,
            #     callback=self.parse_results,
            #     meta={
            #         'BaseState': name,
            #         'Jweller': jweller,
            #         'Address': address,
            #         'State': statecode,
            #         'City': city,
            #         'Zip': zip,
            #         'Phone Number': phone
            #     },
            #     headers={
            #         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
            #     }
            # )

        nextpage = response.xpath("(//ul[@class='pagination']/li/a)[last()]/@href").get()
        if nextpage:
            yield SeleniumRequest(
                url=nextpage,
                wait_time=10,
                callback=self.product_comment,
                meta={'Name': name},
                headers={
                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
                }
            )