# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class ScrollspiderSpider(scrapy.Spider):
    name = 'scrollspider'
    allowed_domains = ['quotes.toscrape.com']
    # start_urls = ['https://quotes.toscrape.com/scroll/']

    script = '''
            function main(splash, args)
              local num_scroll = 13
              local scroll_delay = 1
              
              local scroll_to = splash:jsfunc("window.scrollTo")
              local get_body_hgt = splash:jsfunc(
              "function()	{return document.body.scrollHeight;}"
              )
              
              assert(splash:go(args.url))  
              assert(splash:wait(0.5))
              
              for _=1,num_scroll do
                local height = get_body_hgt()
                for i=1,13 do
                  scroll_to(0,height * i/13)
                  splash:wait(scroll_delay/13)
                end
              end 
              splash:set_viewport_full()
              return splash:html()

            end
        '''

    def start_requests(self):
        yield SplashRequest(
            url="https://quotes.toscrape.com/scroll",
            callback= self.parse,
            endpoint= "execute",
            args= {
                'lua_source': self.script
            }
        )



    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            quote_text = quote.xpath(".//span[@class='text']/text()").get()
            yield {
                'Quote':quote_text
            }

