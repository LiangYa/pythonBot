# 获取新平台对话列表
import csv
import json
import re
import xlwt
import pandas as pd

from config import constants
from config.settings import DM_IP_NEW
from util import request_util
from util.logger import Logger


def getDialogueList(workspace_id, dialogue_id, cookie):
    sessionId = "122222"
    url = "{}/dialogue/startForOutbound?sessionId={}&workspaceId={}&userId={}&dialogueId={}"\
        .format(DM_IP_NEW, sessionId, workspace_id, sessionId, dialogue_id)
    logPredix = "[对话-新平台][获取对话列表]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get(url, cookie)
    json = response.json()
    # Logger.info(json)
    return json


def getFile():
    versionList = []
    with open("../excel/version.csv", mode='r') as csvFile:
        rows = csv.reader(csvFile)
        i = 0
        for row in rows:
            if i == 0:
                row.append("版本号")
                row.append("声模")
            else:
                try:
                    cookie = "1"
                    result = getDialogueList(row[2], row[4], cookie)
                    reply = result["reply"]
                    if ']' in reply:
                        reply = reply.split("]")[0] + "]"
                        pattern = re.compile('\[(.*)\]')
                        version = pattern.search(reply)
                        if '[' in version.group():
                            row.append(version.group().replace("[", "").replace("]", ""))
                        else:
                            row.append("")
                    ttsModel = json.loads(row[9])
                    ttsModel = ttsModel["ttsModel"]
                    row[9] = ttsModel
                    row.append(constants.LABEL_TTS.get(ttsModel))
                except Exception as e:
                    print("error:{}", row)
                    row.append("")
                    row.append("")
            versionList.append(row)
            i = i + 1

    with open("../excel/version2.csv", mode='w') as file2:
        writer = csv.writer(file2)
        writer.writerows(versionList)


    # 修改值
    # df.loc[df['入店来源'].str.find('手淘搜索') > -1, '搜索关键字'] = df['入店来源'].str.replace('手淘搜索', '')
    # df.loc[df['入店来源'].str.find('手淘搜索') > -1, '入店来源'] = '手淘搜索'


    # # 写入新的Excel中
    # list_excel = []
    # list_excel.append(df)
    #
    # writer = pd.ExcelWriter('test2.xlsx')
    # pd.concat(list_excel).to_excel(writer, 'sheet1', index=False)
    # writer.save()
    return "json"


if __name__ == '__main__':
    cookie = "1"
    getFile()
    # print(ttt.group())

    pass
