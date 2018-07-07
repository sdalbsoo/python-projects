import requests
import time
import json


class Watcher():
    slack_url = "https://hooks.slack.com/services/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"  # noqa

    def __init__(self, url, text):
        self.url = url
        self.data = json.dumps({"text": f"{self.url}" + text})
        self.last_content = None

    def check(self):
        resp = requests.get(self.url)
        if self.last_content is None:
            self.last_content = resp.content
            print(f"[{self.url}] Start monitoring!")
        elif self.last_content != resp.content:
            requests.post(
                Watcher.slack_url,
                data=self.data,
                headers={"Content-type": "application/json"}
                )
            self.last_content = resp.content
            print(f"[{self.url}] {self.text}")
        else:
            print(f"[{self.url}] Nothing changed!")


watch_list = [
    # Watcher(url="http://localhost:8000", text="공지가 업데이트됐습니다."),  # noqa
    Watcher(url="http://cse.kongju.ac.kr/community/notice.asp", text="공지가 업데이트됐습니다."),  # noqa
    Watcher(url="http://ie.snu.ac.kr/ko/board/7", text="공지가 업데이트됐습니다."),
    # Watcher(url="http://onenable.tumblr.com/OnePiece", text="원피스 최신화가 업데이트됐습니다."),   # noqa
]

while 1:
    for watch in watch_list:
        watch.check()
    time.sleep(1)
