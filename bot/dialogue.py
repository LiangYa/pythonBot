import requests

from bot import dialogue
from bot.intent import getIntentList
from util import request_util
from config.settings import DM_IP_NEW


# 获取旧平台对话列表
def getDialogueFromOld(workspace_id, cookie):
    url = "http://8.142.85.77:8630/config/dialogue/list?workspaceId={}".format(workspace_id)
    headers = {
        'Cookie': cookie,
        'Host': '8.142.85.77:8630',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    response = requests.get(url, timeout=5, headers=headers)
    json = response.json()
    print(json)
    return json["result"]


def getDialogueList(workspace_id, version_id, cookie):
    url = "{}/configNew/dialogue/list?workspaceId={}&versionId={}"\
        .format(DM_IP_NEW,workspace_id, version_id)
    headers = {
        'Cookie': cookie,
        'Host': '39.99.244.42:18631',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    response = requests.get(url, timeout=5, headers=headers)
    json = response.json()
    print(json)
    return json["result"]


# 添加对话
def addDialogue(name, description, workspace_id, version_id, cookie):
    url = "{}/configNew/dialogue/add".format(DM_IP_NEW)
    data = {
        "name": name,
        "description": description,
        "workspaceId": workspace_id,
        "versionId": version_id,
    }
    response = request_util.post(url, data, cookie)
    print(response.json())
    return response.json()["result"]


def updateDialogue(id, description, workspace_id, version_id, cookie):
    url = "{}/configNew/dialogue/updateDescription".format(DM_IP_NEW)
    data = {
            "id": id,
            "description": description,
            "workspaceId": workspace_id,
            "versionId": version_id,
        }
    response = request_util.post(url, data, cookie)
    print(response.json())


# 添加意图和对话关系
def addRelationShipIntentAndDialogue(dialogue_id, intend_id, workspace_id, version_id, cookie):
    url = "{}/configNew/dialogueAccess/add".format(DM_IP_NEW)
    data = {
        "dialogueId": dialogue_id,
        "accessType": 'INTENT',
        "accessId": intend_id,
        "workspaceId": workspace_id,
        "versionId": version_id,
    }
    response = request_util.post(url, data, cookie)
    print(response.json())


# (通过意图创建对话列表)
def copyDialogue(workspace_id, version_id, old_cookie, cookie):
    intentList = getIntentList(workspace_id, version_id, cookie)
    for one in intentList:
        dialogue = addDialogue(one["name"], one["description"], workspace_id, version_id, cookie)
        updateDialogue(dialogue["id"], dialogue["id"], workspace_id, version_id, cookie)
        addRelationShipIntentAndDialogue(dialogue["id"], one["id"], workspace_id, version_id, cookie)
    pass


# 更新对话ID
def updateDia(cookie):
    dialogueList = dialogue.getDialogueList(637620, 656789, cookie)
    for dialogue1 in dialogueList:
        updateDialogue(dialogue1["id"], dialogue1["id"], 637620, 656789, cookie)


if __name__ == '__main__':
    old_cookie = 'JSESSIONID=node04w0gsef2m6i0w9g9q7omt3ch937603.node0'
    cookie = 'JSESSIONID=node011wd5ha4ikvw8jv4qvreto1nv3178787.node0'
    # copyDialogue(20717, 23487, old_cookie, cookie)
    updateDia(cookie)
