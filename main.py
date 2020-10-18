from scrapy import cmdline
import sys
import time
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


def run_spider(path_file_py, path_file_json):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), path_file_json)
    if os.path.exists(path):
        os.remove(path)
    cmdline.execute("scrapy runspider {} --output={} -L WARNING".format(path_file_py, path_file_json).split())


def correct_links(context):
    correct_hrefs = []
    for item in context['sites']:
        try:
            url = requests.head(item['href'], allow_redirects=True).url
        except requests.exceptions.ConnectionError:
            print('ConnectionError with href = {}'.format(item['href']))
        correct_hrefs.append(url)

    with open('correct_urls.json', 'w') as file:
        file.write(json.dumps(correct_hrefs))


def check_datetime(context):
    time = dt.datetime.now()
    for url in context['sites']:
        datetime_str = url['datetime']
        datetime_i = dt.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    #   if not (datetime_i.month==10 or (datetime_i.month == 9 and datetime_i.day >= time.day)):
    #       print(datetime_i)  # 2018-08-19


def text_preprocessing():
    with open('text.json', 'r') as file:
        file_text = json.loads(file.read())
    all_text = ' '.join([item['text'] for item in file_text])
    all_text = all_text.lower()
    spec_chars = string.punctuation + '\n\xa0«»\t—…'
    all_text = "".join([ch for ch in all_text if ch not in spec_chars])
    text_tokens = word_tokenize(all_text)
    eng_stopwords = stopwords.words("english")
    eng_stopwords.extend(['’', '“', '”'])
    text_tokens_clear = [token.strip() for token in text_tokens if token not in eng_stopwords]
    text_clear = nltk.Text(text_tokens_clear)
    # fdist = FreqDist(text_clear)
    # fdist.plot(30, cumulative=False)
    # print(fdist.most_common(5))
    return " ".join(text_clear)


def make_word_cloud(text):
    wordcloud = WordCloud(width=1000, height=1000,
                          background_color='white',
                          min_font_size=10).generate(text)
    plt.figure(figsize=(5, 5), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()


# uncomment it for a new data
# run_spider(sys.argv[1], 'data.json')
with open('data.json', 'r') as file:
    context = {
        'sites': json.loads(file.read()),
    }
check_datetime(context)
# correct_links(context)
# run spider  parse_links.py
# run_spider(sys.argv[2], 'text.json')
text = text_preprocessing()
make_word_cloud(text)
