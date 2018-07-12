from abc import ABC
from abc import abstractmethod
import json

import requests


class SlackMessage():
    slack_url = "https://hooks.slack.com/services/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"  # noqa

    def send(self, template):
        requests.post(
            SlackMessage.slack_url,
            data=template.data,
            headers={"Content-type": "application/json"}
        )
        print("메세지가 보내졌습니다!\n"+str(template))


class SlackMessageTemplate(ABC):
    @property
    @abstractmethod
    def data(self):
        pass


class NotiTemplate(SlackMessageTemplate):
    def __init__(self, pretext, text, title, title_link, color):
        self._data_dict = {
                "attachments": [
                    {"pretext": pretext,
                     "text": text,
                     "title": title,
                     "title_link": title_link,
                     "color": color,
                     }
                ]
            }
        self._data = json.dumps(self._data_dict)

    @property
    def data(self):
        # TODO study getter
        return self._data

    def __str__(self):
        msg = f"{self._data_dict['attachments'][0]['pretext']}\n"
        msg += f"| {self._data_dict['attachments'][0]['title']}({self._data_dict['attachments'][0]['title_link']})\n"  # noqa
        msg += f"| {self._data_dict['attachments'][0]['text']}"
        return msg

    def __repr__(self):
        return str(self)
