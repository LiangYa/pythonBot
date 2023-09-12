# 从旧平台获取对话列表
from config.settings import SALE_XI_AI_TWO
from util import request_util


def getDialogueFromOld(cookie):
    url = "{}/admin/robotProcess/query".format(SALE_XI_AI_TWO)
    logPredix = "[对话-旧平台][获取旧平台对话列表]{}".format(url)
    data = {
        "companyId": 2217,
        "page": 1,
        "pageSize": 50,
    }
    response = request_util.post_json(url, data, cookie)
    json = response.json()
    return json["data"]["list"]


def getDialogue(cookie):
    lists = getDialogueFromOld(cookie)
    dialogueIds = ""
    for one in lists:
        dialogueIds = "{},{}".format(dialogueIds, one['dialogueId'])
    print(dialogueIds)


if __name__ == '__main__':
    cookie = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsInVzZXJOYW1lIjoiYWRtaW4iLCJzdWIiOiIxNjg0NzQ5MjUyNTUwIiwiaWF0IjoxNjg0NzQ5MjUyfQ.jnFvdJ3rDXnExejwvWTv5LoaG0c4JUSMZH5deZf5JDA"
    getDialogue(cookie)
    pass
