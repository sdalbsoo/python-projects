from bs4 import BeautifulSoup
import requests
import time
import json

colormap = {
    "red": "#C70039",
    "blue": "#334FFF",
    "yellow": "#FFED17",
    "sky": "#2ECCFA",
}


class Watcher():
    slack_url = "https://hooks.slack.com/services/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"  # noqa
    def __init__(self, url, pretext, text, title, title_link, color):
        self.url = url
        self._data = {"text": f"[{self.url}] {text}"}
        self.data = json.dumps(
            {
                "attachments":
                [
                    {"pretext": pretext,
                     "title": title,
                     "title_link": title_link,
                     "text": text,
                     "color": color }
                ]
            }
        )
        self.last_content = None
        self.text = text

    def check(self):
        resp = requests.get(self.url)
        parsed_content = self.parse(resp)
        if self.last_content is None:
            self.last_content = parsed_content
            print(f"[{self.url}] Start monitoring!")
        elif self.last_content != parsed_content:
            # TODO refactor this slack message
            requests.post(
                Watcher.slack_url,
                data=self.data,
                headers={"Content-type": "application/json"}
                )
            self.last_content = parsed_content
            print(f"{self._data}")
        else:
            print(f"[{self.url}] Nothing changed!")

class SnuWatcher(Watcher):
    def parse(self, resp):
        source_snu = resp.text
        soup_snu = BeautifulSoup(source_snu, 'lxml')
        content_ = soup_snu.find('section')
        temp = content_.findAll('td', class_='views-field views-field-title-field')  # noqa
        snu_content = [v.find('a').text for v in temp]
        parsed = snu_content
        return parsed

class LocalWatcher(Watcher):
    def parse(self, resp):
        source_local = resp.text
        soup_local = BeautifulSoup(source_local, 'lxml')
        local_content = soup_local.find('ul')
        parsed = local_content
        return parsed


watch_list = [
    LocalWatcher(url="http://localhost:8000",
                 pretext=f"@sdalbsoo님! 확인 바랍니다.",
                 text="공지가 업데이트됐습니다.",
                 title="local watch!",
                 title_link="http://localhost:8000",
                 color=colormap["sky"],
                 ),  # noqa
    # Watcher(url="http://cse.kongju.ac.kr/community/notice.asp", text="공지가 업데이트됐습니다.",),  # noqa
    SnuWatcher(url="http://ie.snu.ac.kr/ko/board/7",
               pretext=f"@sharsta님! 확인 바랍니다.",
               text="공지가 업데이트됐습니다.",
               title="서울대 공지!",
               title_link="http://ie.snu.ac.kr/ko/board/7",
               color=colormap["sky"],
               ),
    # Watcher(url="http://onenable.tumblr.com/OnePiece", text="원피스 최신화가 업데이트됐습니다."),   # noqa
]

while 1:
    for watch in watch_list:
        watch.check()
    time.sleep(10800)
