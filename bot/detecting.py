import time

from bs4 import BeautifulSoup
import requests

from common.slack import SlackMessage
from common.slack import NotiTemplate


colormap = {
    "red": "#C70039",
    "blue": "#334FFF",
    "yellow": "#FFED17",
    "sky": "#2ECCFA",
}

<<<<<<< HEAD
||||||| merged common ancestors
class Watcher():
    slack_url = "https://hooks.slack.com/services/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"  # noqa
=======
class Watcher():
    slack_url = "https://hooks.slack.com/services/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"  # noqa
>>>>>>> master

class Watcher():
    def __init__(self, url, template):
        self.url = url
        self.slack_msg = SlackMessage()
        self.template = template

        self.last_content = None

    def check(self):
        try:
            resp = requests.get(self.url)
            source = resp.text
            soup = BeautifulSoup(source, 'lxml')
            parsed_content = self.parse(soup)
            if self.last_content is None:
                self.last_content = parsed_content
                print(f"[{self.url}] Start monitoring!")
            elif self.last_content != parsed_content:
                self.slack_msg.send(self.template)
                self.last_content = parsed_content
                print("변화생김")
            else:
                print(f"[{self.url}] Nothing changed!")
        except requests.exceptions.ConnectionError:
            print(f"[{self.url}] 연결이 끊겼습니다.")


class SnuWatcher(Watcher):
    def __init__(self, url, template):
        super(SnuWatcher, self).__init__(url, template)  # noqa

    def parse(self, soup):
        content = soup.find('section')
        temp = content.findAll('td', class_='views-field views-field-title-field')  # noqa
        parsed = [v.find('a').text for v in temp]
        return parsed


class LocalWatcher(Watcher):
    def __init__(self, url, template):
        super(LocalWatcher, self).__init__(url, template)  # noqa

    def parse(self, soup):
        content = soup.find('ul')
        parsed = content
        return parsed


class OnePieceWatcher(Watcher):
    def __init__(self, url, template):
        super(OnePieceWatcher, self).__init__(url, template)  # noqa

    def parse(self, soup):
        content = soup.findAll('a')
        parsed = content
        return parsed


class KongjuWatcher(Watcher):
    def __init__(self, url, template):
        super(KongjuWatcher, self).__init__(url, template)  # noqa

    def parse(self, soup):
        content = soup.findAll('td', class_='lmcNotice')
        parsed = content
        return parsed


def main():
    watch_list = [
        LocalWatcher(
            url="http://localhost:8000",
            template=NotiTemplate(
                pretext=f"@sdalbsoo님! 확인 바랍니다.",
                text="컴퓨터가 업데이됐습니다.",
                title="local watch!",
                title_link="http://localhost:8000",
                color=colormap["sky"],
            )
        ),
         KongjuWatcher(
             url="http://cse.kongju.ac.kr/community/notice.asp",
             template=NotiTemplate(
                 pretext=f"@sdalbsoo님! 확인바랍니다.",
                 text="공지가 업데이트됐습니다.",
                 title="공주대 공지!",
                 title_link="http://cse.kongju.ac.kr/community/notice.asp",  # noqa
                 color=colormap["sky"],
             ),
         ),
        SnuWatcher(
            url="http://ie.snu.ac.kr/ko/board/7",
            template=NotiTemplate(
                pretext=f"@shasta님! 확인 바랍니다.",
                text="공지가 업데이트됐습니다.",
                title="서울대 공지!",
                title_link="http://ie.snu.ac.kr/ko/board/7",
                color=colormap["sky"],
            )
        ),
        # OnePieceWatcher(
            # url="http://onenable.tumblr.com/OnePiece",
            # template=NotiTemplate(
                # pretext=f"확인 바랍니다.",
                # text="원피스 최신화가 업데이트됐습니다.",
                # title="원피스 최신화!",
                # title_link="http://onenable.tumblr.com/OnePiece",
                # color=colormap["yellow"],
            # ),
        # )
    ]
    while 1:
        for watch in watch_list:
            watch.check()
        time.sleep(5)


if __name__ == "__main__":
    main()
