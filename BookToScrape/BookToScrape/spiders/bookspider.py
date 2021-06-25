import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookspiderSpider(CrawlSpider):
    name = 'bookspider'
    allowed_domains = ['books.toscrape.com']
    # start_urls = ['https://books.toscrape.com/']

    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"

    def start_requests(self):
            yield scrapy.Request(url="https://books.toscrape.com", headers={
            'User-Agent': self.agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3/a"), callback='parse_item', follow=True,process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//a[text()='next']"), process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.agent
        return request

    def parse_item(self, response):
        title = response.xpath("//h1/text()").get()
        price = response.xpath("//p[@class='price_color']/text()").get()
        yield {
            'Title': title,
            'Price': price,
            'User-Agent': response.request.headers['User-Agent']
        }
