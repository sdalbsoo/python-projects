import requests
import time
import json

url = "https://hooks.slack.com/services/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"  # noqa

detect_url = "http://cse.kongju.ac.kr/community/notice.asp"
headers = {"Content-type": "application/json"}
data1 = {"text": f"{detect_url} : 공지가 업데이트됐습니다."}
data1_json = json.dumps(data1)

detect_onepiece = "http://onenable.tumblr.com/OnePiece"
headers_onepiece = {"Content-type": "application/json"}
data_onepiece = {"text": f"{detect_onepiece}: 원피스 최신화가 업데이트됐습니다."}   # noqa
data_onepiece_json = json.dumps(data_onepiece)

past_memo = None
past_onepiece_memo = None

while 1:
    rec_memo = requests.get("http://cse.kongju.ac.kr/community/notice.asp")
    if past_memo is None:
        past_memo = rec_memo.content
        continue
    elif rec_memo.content != past_memo:
        requests.post(url, data = data1_json, headers = headers)
        past_memo = rec_memo.content

    rec_onepiece_memo = requests.get("http://onenable.tumblr.com/OnePiece")
    if past_onepiece_memo is None:
        past_onepiece_memo = rec_onepiece_memo.content
        continue
    elif rec_onepiece_memo.content != past_onepiece_memo:
        requests.post(url, data = data_onepiece_json, headers = headers_onepiece)   # noqa
        past_onepiece_memo = rec_onepiece_memo.content

    time.sleep(3600)
