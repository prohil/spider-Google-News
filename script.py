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
            #data = json.loads(response.body)
            #print(data)

        # if data['has_next']:
        #    next_page = data['page'] + 1
        #    yield scrapy.Request(self.quotes_base_url % next_page)

        # for car_div in response.css('.ListingItem-module__main'):

        # link = car_div.css('a.ListingItemTitle-module__link')
        # title = link.css('::text').get()
        # href = link.css('::attr(href)').get()

        # Some prices in span tag, some in div tag
        # raw_price = car_div.css('.ListingItemPrice-module__content::text').get()
        # if not raw_price:
        #    raw_price = car_div.css('.ListingItemPrice-module__content').css('span::text').get()

        ##clear unexpected symbols
        # price = raw_price and clean_price(raw_price) or None
        # img_urls = car_div.css('.Brazzers__image::attr(data-src)').getall()
        # 'title': title,
        # 'href': href,
        # 'price': price,
        # 'imgs': [response.urljoin(img) for img in img_urls],

#       for next_page in response.css('a.next-posts-link'):
#           yield response.follow(next_page, self.parse)
