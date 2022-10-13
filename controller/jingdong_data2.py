import csv
import datetime

import requests
import json


def get_complain():
    complain_str = ""
    dm_url = "http://8.142.85.77:8630/report/getDetailedRecord/?sessionId={}&workSpaceId=8660"
    # dm_url = "http://172.26.2.56:8630/report/getDetailedRecord/?sessionId={}&workSpaceId=8660"
    midTime = "2022-09-10 12:00:00"
    with open("../excel/AC.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            sessionId = row[0]
            if sessionId:
                try:
                    dm_content_json = json.loads(requests.get(dm_url.format(sessionId)).text)
                    for d in dm_content_json['result']:
                        if midTime > d["msgTime"]:
                            print("上午：{}".format(d['msgContent']))
                            break
                        if d['msgContent'] and ("[ROBOT:SJBE]" in d['msgContent']
                                                or "[ROBOT:SJBD]" in d['msgContent']
                                                or "[ROBOT:ZD]" in d['msgContent']):
                            print("通过：{}".format(d['msgContent']))
                            pass
                        else:
                            complain_str = "{},'{}'".format(complain_str, sessionId)
                            break
                        break
                except Exception as e:
                    print("{} not get dm context".format(sessionId))
    print("完成！：{}".format(complain_str))
    with open("{}_complain.txt".format("25-29"), 'a+') as f:
        f.write(complain_str)


def get_complain11():
    complain_str = ""
    dm_url = "http://8.142.85.77:8630/report/getDetailedRecord/?sessionId={}&workSpaceId=8660"
    # dm_url = "http://172.26.2.56:8630/report/getDetailedRecord/?sessionId={}&workSpaceId=8660"
    midTime = "2022-09-10 12:00:00"
    with open("../excel/123.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            sessionId = row[0]
            if sessionId:
                try:
                    dm_content_json = json.loads(requests.get(dm_url.format(sessionId)).text)
                    for d in dm_content_json['result']:
                        if d['msgContent'] and ("元" in d['msgContent']):
                            print("通过：{}".format(d['msgContent']))
                            complain_str = "{},'{}'".format(complain_str, sessionId)
                            break

                except Exception as e:
                    print("{} not get dm context".format(sessionId))
    print("完成！：{}".format(complain_str))
    with open("{}_complain.txt".format("25-29"), 'a+') as f:
        f.write(complain_str)


if __name__ == "__main__":
    get_complain11()




