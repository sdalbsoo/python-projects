import requests
import json


class SlackMessage():
    slack_url = "https://hooks.slack.com/services/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"  # noqa

    def send(self, url, pretext, text, title, title_link, color):
        data = json.dumps(
            {
                "attachments": [
                    {"pretext": pretext,
                     "text": text,
                     "title": title,
                     "title_link": title_link,
                     "color": color,
                     }
                ]
            }
        )
        requests.post(
            SlackMessage.slack_url,
            data=data,
            headers={"Content-type": "application/json"}
        )
        print(f"[{url}] {text}")
