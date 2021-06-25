import scrapy
from scrapy_splash import SplashRequest


class NewsspiderSpider(scrapy.Spider):
    name = 'newsspider'
    allowed_domains = ['www.imdb.com']
    # start_urls = ['https://www.imdb.com/news/movie    /?ref_=nv_nw_mv/']

    script = '''
            function main(splash, args)
              assert(splash:go(args.url))
              assert(splash:wait(0.5))
              for i=1,15,1 do
                    btn = splash:select("#news-load-more")
                    assert(btn:mouse_click())
                    assert(splash:wait(2))
              end
              
              return {
                html = splash:html()
              }
            end
        '''

    def start_requests(self):
        yield SplashRequest(
            url="https://www.imdb.com/news/movie/?ref_=nv_nw_mv",
            callback=self.parse,
            endpoint="execute",
            args={
                'lua_source': self.script
            }
        )

    def parse(self, response):
        all_news = response.xpath("//h2[@class='news-article__title']")
        for news in all_news:
            yield {
                'News': news.xpath(".//a/text()").get()
            }
