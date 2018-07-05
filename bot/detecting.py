import requests
import time
import json

url = "https://hooks.slack.com/services/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" 
headers = {"Content-type" : "application/json"}
data1 = {"text" : "변화가 감지되었습니다."}
data2 = {"text" : "변화가 감지되지 않았습니다."}
data1_json = json.dumps(data1)
data2_json = json.dumps(data2)

past_memo = None
while 1:
    rec_memo = requests.get('http://0.0.0.0:8000/')
    if past_memo == None:
        past_memo = rec_memo.content
        continue
    elif rec_memo.content != past_memo:
        requests.post("https://hooks.slack.com/services/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", data=data1_json, headers=headers)
        past_memo = rec_memo.content
    else:
        requests.post("https://hooks.slack.com/services/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", data=data2_json, headers=headers)
    time.sleep(4)
