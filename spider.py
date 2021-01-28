import requests
import re
import pdfkit
import os
from bs4 import BeautifulSoup

MAX_CATCHING = 5


def get_header():
    return {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 "
                      "Safari/537.36",
        'Host': "www.zhihu.com",
        'Origin': "https://www.zhihu.com",
        'Pragma': "no-cache",
        'Referer': "https://www.zhihu.com/"
    }


class Question:
    def __init__(self, url):
        if not re.compile(r"(http|https)://www.zhihu.com/question/\d{8}").match(url):
            raise ValueError("Invalid zhihu question uri:\"{url}\"".format(url=url))
        else:
            self.contents = {}
            self.url = url
            #self.id = url[len(url) - 8:]
            self.id = re.compile(r"(http|https)://www.zhihu.com/question/(\S+)").match(url).group(2)
            self.start_requests()

    def start_requests(self):
        url = 'https://www.zhihu.com/api/v4/questions/' + self.id
        r = requests.get(url, headers=get_header()).json()
        self.title = r['title']
        url += '/answers'
        curr = 0
        while 1:

            r = requests.get(url, headers=get_header()).json()
            for content in r['data']:
                slug = re.compile(r"(http|https)://www.zhihu.com/api/v4/answers/(\S+)").match(content['url']).group(2)
                u = 'https://www.zhihu.com/question/' + self.id + '/answer/' + slug
                self.contents[content['id']] = {
                    'answer': Answer(u),
                    'author': content['author']['name']
                }
            curr += 1
            if r['paging']['is_end'] or curr == MAX_CATCHING:
                break

            url = r['paging']['next']


    def get_title(self):
        return self.title

    def get_answer_ids(self):
        return self.contents.keys()

    def save_to_pdf(self, id, path):
        self.contents[id]['answer'].save_to_pdf(path)

    def save_all(self):
        os.mkdir(self.title)
        for id in self.contents:
            c = self.contents[id]
            c['answer'].save_to_pdf(self.title + '/' + c['author'] + '\'s answer.pdf')


class Column:
    def __init__(self, url):
        self.contents = {}
        if not re.compile(r"(http|https)://www.zhihu.com/column/\S+").match(url):
            raise ValueError("\"" + url + "\"" + " : it isn't a column url.")
        else:
            self.url = url
            self.slug = re.compile(r"(http|https)://www.zhihu.com/column/(\S+)").match(url).group(2)
            self.parse()

    def parse(self):
        url = "https://www.zhihu.com/api/v4/columns/" + self.slug
        r = requests.get(url, headers=get_header()).json()
        self.title = r['title']
        curr = 0
        url += "/articles"
        while 1:
            r = requests.get(url, headers=get_header())
            j = r.json()
            data = j['data']
            for article in data:
                self.contents[article['title']] = article['content']

            curr += 1
            if j['paging']['is_end'] or curr == MAX_CATCHING:
                break

            url = j['paging']['next']

    def get_title(self):
        return self.title

    def get_titles(self):
        return self.contents.keys()

    def save_to_pdf(self, title, path):
        pdfkit.from_string('<head><meta charset="UTF-8"></head>' + self.contents[title], path)

    def save_all(self):
        os.mkdir(self.slug)
        for title in self.contents:
            pdfkit.from_string('<head><meta charset="UTF-8"></head>' + self.contents[title],
                               self.slug + '/' + title + '.pdf')


class Answer:
    def __init__(self, url):
        if not re.compile(r"(http|https)://www.zhihu.com/question/(\S+)/answer/(\S+)").match(url):
            raise ValueError("Invalid zhihu answer uri:\"{url}\"".format(url=url))
        self.url = url

    def save_to_pdf(self, path):
        r = requests.get(self.url, headers=get_header()).content
        bs = BeautifulSoup(r, 'lxml')
        pdfkit.from_string(
            '<head><meta charset="UTF-8"></head>' + str(bs.find_all('div', class_='RichContent-inner')[0]), path)

