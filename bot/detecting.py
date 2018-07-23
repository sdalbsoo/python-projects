import time
from abc import abstractmethod
from abc import ABC

from bs4 import BeautifulSoup
import requests

from common.slack import SlackMessage
from common.slack import NotiTemplate
from common.utils import get_logger


colormap = {
    "red": "#C70039",
    "blue": "#334FFF",
    "yellow": "#FFED17",
    "sky": "#2ECCFA",
}


class Watcher(ABC):
    def __init__(self, url, template):
        self.url = url
        self.slack_msg = SlackMessage()
        self.template = template
        self.log = get_logger(__name__)

        self.last_content = None

    def check(self):
        try:
            parsed_content = self.parse(self.crawl())
            if self.last_content is None:
                self.last_content = parsed_content
                self.log.info(f"[{self.url}] Start Monitoring!")
            elif self.last_content != parsed_content:
                self.slack_msg.send(self.template)
                self.last_content = parsed_content
                self.log.info(f"[{self.url}] something changed!")
            else:
                self.log.info(f"[{self.url}] Nothing changed!")
        except requests.exceptions.ConnectionError:
            self.log.info(f"[{self.url}] Disconnecting!")

    def crawl(self):
        resp = requests.get(self.url)
        source = resp.text
        soup = BeautifulSoup(source, 'lxml')
        return soup

    @abstractmethod
    def parse(self):
        pass


class KongjuStudentWatcher(Watcher):
    def __init__(self, url, template):
        super(KongjuStudentWatcher, self).__init__(url, template)

    def parse(self, soup):
        content = soup.findAll('td', class_='table_td2')
        parsed = content
        return parsed


class SBCWatcher(Watcher):
    def __init__(self, url, template):
        super(SBCWatcher, self).__init__(url, template)

    def crawl(self):
        payload = "{\"pageInfo\":{\"nowPage\":\"1\",\"pageCount\":10,\"rowCount\":10,\"maxPage\":\"\",\"searchC\":\"\",\"searchG\":\"\",\"searchT\":\"\",\"param\":\"proc=List\",\"resultCd\":\"\",\"resultMsg\>}"  # noqa
        headers = {
            'accept': "application/json",
            'submissionid': "getInfoList",
            'origin': "http://hp.sbc.or.kr",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",  # noqa
            'content-type': "application/json; charset=\"UTF-8\"",
            'referer': "http://hp.sbc.or.kr/websquare/websquare.jsp?w2xPath=/SBC/n_news/notice/notice_list.xml",  # noqa
            'accept-encoding': "gzip, deflate",
            'accept-language': "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            'cookie': "WMONID=GtJw3KRl_Jb; JSESSIONID_SBC=c46sniugt7KHD4fVmzwBJiU91SiB-OyXyeHuqRaFM8i-6EWpNvgw!-900504505; wcs_bt=1076b58a5102e64:1531904537; lastAccess=1531904538020",  # noqa
            'cache-control': "no-cache",
            'postman-token': "883631c4-2fd3-d638-356e-a21e58f04365",
            }
        resp = requests.request("POST", self.url, data=payload, headers=headers)  # noqa
        return resp

    def parse(self, input):
        return input

    def check(self):
        try:
            resp = self.crawl()
            parsed_content = self.parse(resp.text)
            if self.last_content is None:
                self.last_content = parsed_content
                self.log.info(f"[{self.url}] Start Monitoring!")
            elif self.last_content != parsed_content:
                self.slack_msg.send(self.template)
                self.last_content = parsed_content
                self.log.info(f"[{self.url}] something changed!")
            else:
                self.log.info(f"[{self.url}] Nothing changed!")
        except requests.exceptions.ConnectionError:
            self.log.info(f"[{self.url}] Disconnecting!")


class SnuWatcher(Watcher):
    def __init__(self, url, template):
        super(SnuWatcher, self).__init__(url, template)

    def parse(self, soup):
        content = soup.find('section')
        temp = content.findAll('td', class_='views-field views-field-title-field')  # noqa
        parsed = [v.find('a').text for v in temp]
        return parsed


class LocalWatcher(Watcher):
    def __init__(self, url, template):
        super(LocalWatcher, self).__init__(url, template)

    def parse(self, soup):
        content = soup.find('ul')
        parsed = content
        return parsed


class OnePieceWatcher(Watcher):
    def __init__(self, url, template):
        super(OnePieceWatcher, self).__init__(url, template)

    def parse(self, soup):
        content = soup.findAll('a')
        parsed = content
        return parsed


class KongjuWatcher(Watcher):
    def __init__(self, url, template):
        super(KongjuWatcher, self).__init__(url, template)

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
            ),
        ),
        KongjuWatcher(
             url="http://cse.kongju.ac.kr/community/notice.asp",
             template=NotiTemplate(
                 pretext=f"@sdalbsoo님! 확인바랍니다.",
                 text="공지가 업데이트됐습니다.",
                 title="공주대 공지!",
                 title_link="http://cse.kongju.ac.kr/community/notice.asp",
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
            ),
        ),
        OnePieceWatcher(
            url="http://onenable.tumblr.com/OnePiece",
            template=NotiTemplate(
                pretext=f"확인 바랍니다.",
                text="원피스 최신화가 업데이트됐습니다.",
                title="원피스 최신화!",
                title_link="http://onenable.tumblr.com/OnePiece",
                color=colormap["yellow"],
            ),
        ),
        SBCWatcher(
            url="http://hp.sbc.or.kr/news/notice.do",
            template=NotiTemplate(
                pretext=f"@sdalbsoo님! 확인 바랍니다.",
                text="공지가 업데이트됐습니다.",
                title="중소기업 공지!",
                title_link="http://hp.sbc.or.kr/websquare/websquare.jsp?w2xPath=/SBC/n_news/notice/notice_list.xml",  # noqa
                color=colormap["sky"],
            ),
        ),
        KongjuStudentWatcher(
            url="http://www.kongju.ac.kr/lounge/board.jsp?page=0&board=student_news",  # noqa
            template=NotiTemplate(
                pretext=f"@sdalbsoo님! 확인 바랍니다.",
                text="공지가 업데이트됐습니다.",
                title="공주대학교 학생공지!",
                title_link="http://www.kongju.ac.kr/lounge/board.jsp?page=0&board=student_news",  # noqa
                color=colormap["sky"],
            ),
        ),
    ]
    while 1:
        for watch in watch_list:
            watch.check()
        time.sleep(10)


if __name__ == "__main__":
    main()
