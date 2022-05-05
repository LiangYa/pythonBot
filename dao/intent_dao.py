from util import request_util
from config.settings import DM_IP_NEW, DM_IP_OLD
from util.logger import Logger


# 获取意图列表
def getIntentFromOld(workspace_id, cookie):
    url = "{}/config/intent/list?intentClass=NORMAL&workspaceId={}&query=".format(DM_IP_OLD, workspace_id)
    logPredix = "[意图-旧平台][获取意图列表]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get_old(url, cookie)
    json = response.json()
    Logger.info(json)
    return json["result"]


def addIntent(name, description, workspace_id, version_id, cookie):
    url = "{}/configNew/intent/add".format(DM_IP_NEW)
    logPredix = "[意图-新平台][添加意图]{}".format(url)
    Logger.info(logPredix)
    data = {
        "name": name,
        "description": description,
        "workspaceId": workspace_id,
        "versionId": version_id
    }
    response = request_util.post(url, data, cookie)
    Logger.info(response.json())
    return response.json()["result"]


# 获取新平台意图
def getIntentList(workspace_id, version_id, cookie):
    url = "{}/configNew/intent/list?intentClass=NORMAL&workspaceId={}&versionId={}&query="\
        .format(DM_IP_NEW, workspace_id, version_id)
    logPredix = "[意图-新平台][获取意图列表]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get(url, cookie)
    json = response.json()
    Logger.info(json)
    return json["result"]
