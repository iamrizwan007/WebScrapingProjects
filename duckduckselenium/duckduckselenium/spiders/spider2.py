# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest


class SlickspiderSpider2(scrapy.Spider):
    name = 'slickspider2'

    def start_requests(self):
        yield SeleniumRequest(
            url="http://www.buyandsellgoldsilver.com/Gold-Silver-Dealers",
            wait_time=2,
            callback=self.parse
        )

    def parse(self, response):
        products = response.xpath("//div[@class='row'][2]//a")
        for link in products:
            name = link.xpath(".//text()").get()
            href = link.xpath(".//@href").get()
            yield SeleniumRequest(
                url=href,
                wait_time=2,
                callback=self.product_comment_two,
                meta={'Name': name}
            )

        # name = response.xpath("(//div[@class='row'][2]//a)[1]/text()").get()
        # href = response.xpath("(//div[@class='row'][2]//a)[1]/@href").get()
        # yield SeleniumRequest(
        #     url=href,
        #     wait_time=2,
        #     callback=self.product_comment,
        #     meta={'Name': name}
        # )


        # for product in products:
        #     name = product.xpath(".//a[contains(@class,'itemTitle')]/text()").get()
        #     link = product.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']/@href").get()
        #     # yield {
        #     #     'Name': name,
        #     #     'User-Agent': response.request.headers['User-Agent']
        #     # }
        #     absolute = f"https://slickdeals.net{link}"
        #     yield SeleniumRequest(
        #         url= absolute,
        #         wait_time= 2,
        #         callback= self.product_comment,
        #         meta={'Name': name}
        #     )
        #
        # # next_page = response.xpath("//a[@data-role='next-page']/@href").get()
        # if next_page:
        #     abs_url = f"https://slickdeals.net{next_page}"
        #     print(abs_url)
        #     print("***********************")
        #     yield SeleniumRequest(url=abs_url, wait_time=2, callback=self.parse, headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'})

    def product_comment_two(self, response):
        name = response.meta['Name']
        comments = response.xpath("//div[@class='equal-height-content equal-height-box-custom single-row']")
        for com in comments:
            fs = 12
            yield {
                'FullState': name,
                'Jeweller': com.xpath(".//h3/a/text()").get(),
                'Address': com.xpath(".//span[@class='address']/text()").get(),
                'City': com.xpath(".//span[@class='city']/text()").get(),
                'StateCode': com.xpath(".//span[@class='state_code']/text()").get(),
                'Zip': com.xpath(".//span[@class='zip']/text()").get()
            }
            next = response.xpath("(//ul[@class='pagination']/li/a)[last()]/@href").get()
            if next:
                yield SeleniumRequest(url=next,wait_time=2,callback=self.product_comment_two,meta={'Name': name})
        # print('''
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        # .
        #
        #
        # ''')