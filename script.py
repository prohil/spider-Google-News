import scrapy
import json


class GnewsSpider(scrapy.Spider):
    name = 'google_news'
    start_urls = ['https://news.google.com/search?q=russia&hl=en-US&gl=US&ceid=US%3Aen']
    # start_urls = [base_url % 1]
    download_delay = 1.5

    def parse(self, response):
        for news_block in response.css('.NiLAwe'):
            href = news_block.css('a.VDXfz::attr(href)').get()
            datetime = news_block.css('time.WW6dff::attr(datetime)').get()
            yield {
                'href': response.urljoin(href),
                'datetime': datetime,
            }

