import re
import json
import requests
import urllib3
from bs4 import BeautifulSoup
import pdfkit

urllib3.disable_warnings()


class Question:
    url = None
    id = None
    path = None
    soup = None
    title = None

    def __init__(self, url, title):
        if not re.compile(r"(http|https)://www.zhihu.com/question/\d{8}").match(url):
            raise ValueError("Invalid zhihu question uri:\"{url}\"".format(url=url))
        else:
            self.url = url
            self.id = url[len(url) - 8:]
            self.parse()

        if title:
            self.title = title
        else:
            self.title = self.get_question()

        # print(self.soup)

    def get_detail(self):
        if self.soup is None:
            self.parse()
        print(self.soup.find_all("div"))
        detail = self.soup.find("div", id="zh-question-detail").div.get_text().encode("utf-8")
        return detail

    def get_question(self):
        try:
            question = self.soup.find("h1", {"class": "QuestionHeader-title"}).text
        except:
            question = ""

        return question

    def get_tag(self):
        tag_list = []
        try:
            tags = self.soup.find_all("div", {"class": "QuestionTopic"})
            for tag in tags:
                tag_list.append(tag.text)
        except:
            pass
        return tag_list

    def get_answer(self, page):
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/42.0.2311.135 Safari/537.36",
            'Host': "www.zhihu.com",
            'Origin': "http://www.zhihu.com",
            'Pragma': "no-cache",
            'Referer': "http://www.zhihu.com/"
        }
        url = 'https://www.zhihu.com/api/v4/questions/' + self.id + '/answers?include=data%5B%2A%5D.is_normal' \
                                                                    '%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail' \
                                                                    '%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent' \
                                                                    '%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time' \
                                                                    '%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized' \
                                                                    '%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url' \
                                                                    '%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=' + str(
            page) + '&platform=desktop&sort_by=default'
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        json_data = json.loads(r.text)['data']
        for item in json_data:
            pdfkit.from_string(
                '<head><meta charset="UTF-8"></head>' + item['content'], str(item['id']) + '.pdf')
            print(item['id'], item['content'])
        comments = []
        # print(json_data)

    def parse(self):
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/42.0.2311.135 Safari/537.36",
            'Host': "www.zhihu.com",
            'Origin': "http://www.zhihu.com",
            'Pragma': "no-cache",
            'Referer': "http://www.zhihu.com/"
        }

        r = requests.get(self.url, headers=headers, verify=False)
        self.soup = BeautifulSoup(r.content, 'lxml')

# Test
# q = Question('https://www.zhihu.com/question/21217244', None)
# # print(q.get_detail())
# print(q.get_question())
# print(q.get_tag())
# print(q.get_answer(1))
