# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class QuotespiderSpider(scrapy.Spider):
    name = 'quotespider'
    allowed_domains = ['quotes.toscrape.com']
    # start_urls = ['https://quotes.toscrape.com/js/']

    script = '''    
            function main(splash, args)
              url = args.url
              assert(splash:go(url))
             return splash:html()
            end
    '''

    def start_requests(self):
        yield SplashRequest(
            url= "https://quotes.toscrape.com/js",
            callback= self.parse,
            endpoint= "execute",
            args={
                'lua_source': self.script
            }
        )

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            quote_text = (quote.xpath(".//span[@class='text']/text()").get()).strip()
            author = quote.xpath(".//small/text()").get()
            tags = quote.xpath(".//div/a")
            if len(tags) > 1:
                quote_tags = ""
                for tag in tags:
                    quote_tags = quote_tags + " " + tag.xpath(".//text()").get()

                yield {
                    'Quote': quote_text,
                    'Author': author,
                    'Tags': quote_tags
                }
            else:
                yield {
                    'Quote': quote_text,
                    'Author': author,
                    'Tags': response.xpath(".//text()").get()
                }
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if response.xpath("//li[@class='next']/a/@href"):
            next_abs_url = response.urljoin(next_page)

            yield SplashRequest(
                url=next_abs_url,
                callback=self.parse,
                endpoint="execute",
                args={
                    'lua_source': self.script
                }
            )

