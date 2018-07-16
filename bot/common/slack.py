import json
from abc import ABC
from abc import abstractmethod

import requests

from common.utils import get_logger


class SlackMessage():
    slack_url = "https://hooks.slack.com/services/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"  # noqa
    def __init__(self):
        self.log = get_logger(__name__)

    def send(self, template):
       resp = requests.post(
            SlackMessage.slack_url,
            data=template.data,
            headers={"Content-type": "application/json"}
        )
       self.log.info(f"slack message response: {resp.content}")


class SlackMessageTemplate(ABC):
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
        return self._data

    def __str__(self):
        msg = "=" * 44 + "\n"
        msg += f"{self._data_dict['attachments'][0]['pretext']}\n"
        msg += f"| {self._data_dict['attachments'][0]['title']}({self._data_dict['attachments'][0]['title_link']})\n"  # noqa
        msg += f"| {self._data_dict['attachments'][0]['text']}\n"
        msg += "=" * 44
        return msg

    def __repr__(self):
        return str(self)
