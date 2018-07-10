from datetime import timedelta, datetime
import json
import os

import requests


colormap = {
    "red": "#C70039",
    "blue": "#334FFF",
    "green": "#28C640",
    "yellow": "#FFED17",
}
# 감시할 레포
watch_list = [
    {"owner": "sdalbsoo", "repo": "python-practice"},
    {"owner": "sdalbsoo", "repo": "study"},
]
github2slack = {
    "sdalbsoo": "sdalbsoo",
    "shastakr": "shasta",
}

# access_token 을 그냥 코드에 박으면 보안상 위험하다.
# 이 토큰만 있으면 누구나 private repo를 열어볼 수 있기 때문이다.
# 따라서, access_token이라는 환경변수에 os.environ으로 접근해서 가져온다.
# 커맨드라인에서 환경변수를 지정하면서 다음과 같이 코드를 돌릴 수 있다.
#
# access_token=[실제 토큰값 입력] python pr_check.py
#
params = {
    "access_token": os.environ["access_token"]
}
# 간단하게 curl로 Github에 요청을 실험해볼 수 있다.
#
# curl 'https://api.github.com/repos/sdalbsoo/python-practice/pulls?access_token=[access_token]'  # noqa
#
# [access_token] 은 다음 문서에 따라 발급받을 수 있다.
# https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/#creating-a-token  # noqa


class SlackMessage():
    def __init__(self, url=None):
        if url is None:
            self.url = "https://hooks.slack.com/services/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"  # noqa
        else:
            self.url = url

    def send(self, title, text, color):
        # https://api.slack.com/docs/message-formatting
        data = json.dumps(
            {
                "attachments": [
                    {"color": color, "title": title, "text": text, "mrkdwn_in": ["text", "pretext"]},  # noqa
                ]
            }
        )
        requests.post(
            self.url,
            data=data,
            headers={"Content-type": "application/json"}
        )
        print("Send slack message: {title} {text}")


slack = SlackMessage()
now = datetime.now()
for watch in watch_list:
    owner, repo = watch["owner"], watch["repo"]

    # Pull requests 와 관련된 API 명세는 다음 문서에서 볼 수 있다.
    # https://developer.github.com/v3/pulls/#list-pull-requests
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    resp = requests.get(url, params=params)
    resp_dic = json.loads(resp.content.decode("utf-8"))

    for pr in resp_dic:
        pr_user = "@" + github2slack[pr["user"]["login"]]

        pr_url = pr["url"]
        pr_title = pr["title"]
        # Github 에서 주는 시간은 '그리니치 천문대'의 시간이다.
        # 따라서, 한국 시간으로 바꾸기 위해선 항상 9시간을 더해줘야한다.
        pr_created_at = datetime.strptime(
            pr["created_at"], "%Y-%m-%dT%H:%M:%SZ"
        ) + timedelta(hours=9)
        pr_updated_at = datetime.strptime(
            pr["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
        ) + timedelta(hours=9)
        pr_reviewer_id_list = [
            "@"+github2slack[rr["login"]] for rr in pr["requested_reviewers"]
        ]
        pr_reviewers = ", ".join(pr_reviewer_id_list)

        hours_from_created_at = (now - pr_created_at).seconds / 60 / 60
        hours_from_updated_at = (now - pr_updated_at).seconds / 60 / 60

        if len(pr_reviewer_id_list) > 0:
            if 0 <= hours_from_updated_at < 12:
                slack.send(title=f"[{pr_title}]({pr_url})",
                           color=colormap["blue"],
                           text=(f"{pr_reviewers}님! {pr_user}의 코드가 리뷰 대기 중입니다. "  # noqa
                                 f"마지막 업데이트로부터 {hours_from_updated_at:.1f} 시간 흘렀습니다."))  # noqa
            elif 12 <= hours_from_updated_at < 24:
                slack.send(title=f"[{pr_title}]({pr_url})",
                           color=colormap["green"],
                           text=(f"{pr_reviewers}님! {pr_user}의 코드가 리뷰 대기 중입니다. "  # noqa
                                 f"마지막 업데이트로부터 {hours_from_updated_at:.1f} 시간 흘렀습니다."))  # noqa
            elif 24 <= hours_from_updated_at < 48:
                slack.send(title=f"[{pr_title}]({pr_url})",
                           color=colormap["yellow"],
                           text=(f"{pr_reviewers}님! {pr_user}의 코드가 리뷰 대기 중입니다. "  # noqa
                                 f"마지막 업데이트로부터 {hours_from_updated_at:.1f} 시간 흘렀습니다. 빨리 확인하세요!"))  # noqa
            elif 48 <= hours_from_updated_at:
                slack.send(title=f"[{pr_title}]({pr_url})",
                           color=colormap["red"],
                           text=(f"{pr_reviewers}님! {pr_user}의 코드가 리뷰 대기 중입니다. "  # noqa
                                 f"마지막 업데이트로부터 {hours_from_updated_at:.1f} 시간 흘렀습니다. PR이 썩어가요..! 빨리 리뷰해주세요 (ㅠㅠ)"))  # noqa
        else:
            slack.send(title=f"[{pr_title}]({pr_url})",
                       color=colormap["blue"],
                    text=f"0개의 PR이 리뷰 대기 중입니다.")  # noqa
            print(f"아직 리뷰어를 요청하지 않았습니다.")
