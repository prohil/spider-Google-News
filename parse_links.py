import scrapy
import json

class TextNewsSpider(scrapy.Spider):
    name = 'text_news'
    with open('correct_urls.json', 'r') as file:
        context = {
            'sites': json.loads(file.read()),
        }
    start_urls = context['sites']
    download_delay = 1.5

    def parse(self, response):
        allText =''
        for text in response.css('p::text'):
            str_text = text.get()
            if len(str_text.split(' ')) > 5:
                allText += str_text + ' '

        yield {
            'text': allText,
        }
