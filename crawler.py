import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
import datetime as dt
import requests
import string
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def remove_file(path_file_json):
    """Remove file. Scrapy add information to data.json every time it runs"""
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), path_file_json)
    if os.path.exists(path):
        os.remove(path)


def check_datetime(datetime_now, datetime_str):
    """Check if time is last month"""
    datetime = dt.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    if datetime.month == datetime_now.month or (
            datetime.month == datetime_now.month - 1 and datetime.day >= datetime_now.day):
        return True
    else:
        return False


def text_preprocessing(json_text):
    '''Delete english stopwords, symbols and merge json text'''
    all_text = ' '.join([item['text'] for item in json_text])
    all_text = all_text.lower()
    spec_chars = string.punctuation + '\n\xa0«»\t—…'
    all_text = "".join([ch for ch in all_text if ch not in spec_chars])
    text_tokens = word_tokenize(all_text)
    eng_stopwords = stopwords.words("english")
    eng_stopwords.extend(['’', '“', '”'])
    text_tokens_clear = [token.strip() for token in text_tokens if token not in eng_stopwords]
    text_clear = nltk.Text(text_tokens_clear)
    # Uncomment to see word distrubution
    # fdist = FreqDist(text_clear)
    # fdist.plot(30, cumulative=False)
    # print(fdist.most_common(5))
    return " ".join(text_clear)


def make_word_cloud(str):
    """Make word cloud picture from parsed text
    """
    wordcloud = WordCloud(width=1000, height=1000,
                          background_color='white',
                          min_font_size=10).generate(str)
    plt.figure(figsize=(5, 5), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()


class GnewsSpider(scrapy.Spider):
    name = 'google_news'
    start_urls = ['https://news.google.com/search?q=russia&hl=en-US&gl=US&ceid=US%3Aen']
    download_delay = 2.5

    def parse(self, response):
        """Parse main page of google news"""
        count = 0
        selector = response.css('.NiLAwe')
        number_news_block = len(selector.extract())
        print('Find {} urls on the page'.format(number_news_block))
        current_time = dt.datetime.now()
        if selector is not None:
            for news_block in selector:
                href = news_block.css('a.VDXfz::attr(href)').get()
                datetime = news_block.css('time.WW6dff::attr(datetime)').get()
                count += 1
                print('Url {}/{} connection'.format(count, number_news_block))
                if href is not None and check_datetime(current_time, datetime):
                    href = response.urljoin(href)
                    try:
                        url = requests.head(href, allow_redirects=True).url
                        print('Redirected url = ' + url)
                        yield scrapy.Request(url=url, callback=self.parse_p_blocks)
                    except requests.ConnectionError as e:
                        print("Connection Error. Make sure you are connected to Internet. Technical Details given below.\n" + str(e))
                    except requests.Timeout as e:
                        print("Timeout Error"+ "\n" + str(e))
                    except requests.RequestException as e:
                        print("General Error"+ "\n" + str(e))
                    except requests.SSLError as e:
                        print("Max retries exceeded with url" + "\n" + str(e))
                    except Exception as e:
                        print("Unexpected exception" + "\n" + str(e))
                    #except requests.exceptions.ConnectionError:
                    #    print('ConnectionError with href = {}'.format(href))
                else:
                    print('Empty href or wrong time')
            print('Success')
        else:
            print('Something goes wrong')

    def parse_p_blocks(self, response):
        """Parse p blocks on links from google news"""
        selector = response.css('p::text')
        if selector is not None:
            allText = ''
            for text in selector:
                str_text = text.get().strip()
                if len(str_text.split(' ')) > 5:
                    allText += str_text + ' '
            yield {
                'text': allText,
            }
        else:
            print("Empty text from page" + str(response.request.url))


remove_file('data.json')
process = CrawlerProcess(settings={
    "FEEDS": {
        "data.json": {"format": "json"},
    },
})
process.crawl(GnewsSpider)
process.start()  # the script will block here until the crawling is finished

with open('data.json', 'r') as file:
    data = json.loads(file.read())
print('Begin text processing...')
text = text_preprocessing(data)
print('Text processing complete')
print('Word cloud picture is creating...')
make_word_cloud(text)
