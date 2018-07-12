import requests
import json


class SlackMessage():
    slack_url = "https://hooks.slack.com/services/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"  # noqa

    def __init__(self, url, pretext, text, title, title_link, color):
        self.url = url
        self.pretext = pretext
        self.text = text
        self.title = title
        self.title_link = title_link
        self.color = color
        self.data = json.dumps(
            {
                "attachments": [
                    {"pretext": pretext,
                     "text": text,
                     "title": title,
                     "title": title_link,
                     "color": color,
                     }
                ]
            }
        )

    def send(self):
        data = self.data
        requests.post(
            SlackMessage.slack_url,
            data=data,
            headers={"Content-type": "application/json"}
        )
        print(f"[{self.url}] {self.text}")
