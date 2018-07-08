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
        self.data = json.dumps(#self._data
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
        if self.last_content is None:
            self.last_content = resp.content
            print(f"[{self.url}] Start monitoring!")
        elif self.last_content != resp.content:
            # TODO refactor this slack message
            requests.post(
                Watcher.slack_url,
                data=self.data,
                headers={"Content-type": "application/json"}
                )
            self.last_content = resp.content
            print(f"{self._data}")
        else:
            print(f"[{self.url}] Nothing changed!")


watch_list = [
    Watcher(url="http://localhost:8000", pretext=f"@sdalbsoo님! 확인 바랍니다.", text="공지가 업데이트됐습니다.",
            title="공주대 공지!", title_link="http://localhost:8000", color=colormap["sky"],),  # noqa
    # Watcher(url="http://cse.kongju.ac.kr/community/notice.asp", text="공지가 업데이트됐습니다.",),  # noqa
    # Watcher(url="http://ie.snu.ac.kr/ko/board/7", text="공지가 업데이트됐습니다."),
    # Watcher(url="http://onenable.tumblr.com/OnePiece", text="원피스 최신화가 업데이트됐습니다."),   # noqa
]

while 1:
    for watch in watch_list:
        watch.check()
    time.sleep(5)
