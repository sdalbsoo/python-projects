import requests
import time
import json

detect_url = "http://cse.kongju.ac.kr/community/notice.asp"
url = "https://hooks.slack.com/services/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" 
headers = {"Content-type" : "application/json"}
data1 = {"text" : f"{detect_url} : 공지가 업데이트됐습니다."} 
data1_json = json.dumps(data1)

past_memo = None
while 1:
    rec_memo = requests.get("http://cse.kongju.ac.kr/community/notice.asp")
    if past_memo == None:
        past_memo = rec_memo.content
        continue
    elif rec_memo.content != past_memo:
        requests.post("https://hooks.slack.com/services/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", data=data1_json, headers=headers)
        past_memo = rec_memo.content
    time.sleep(3600)
