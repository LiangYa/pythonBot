from config.settings import DM_IP_OLD, DM_IP_NEW
from util import request_util
from util.logger import Logger


# 从旧平台获取对话列表
def getDialogueFromOld(workspace_id, cookie):
    url = "{}/config/dialogue/list?workspaceId={}".format(DM_IP_OLD, workspace_id)
    logPredix = "[对话-旧平台][获取旧平台对话列表]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get_old(url, cookie)
    json = response.json()
    Logger.info(json)
    return json["result"]


# 获取新平台对话列表
def getDialogueList(workspace_id, version_id, cookie):
    url = "{}/configNew/dialogue/list?workspaceId={}&versionId={}".format(DM_IP_NEW, workspace_id, version_id)
    logPredix = "[对话-新平台][获取对话列表]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get(url, cookie)
    json = response.json()
    # Logger.info(json)
    return json["result"]


# 新平台-添加对话
def addDialogue(name, description, workspace_id, version_id, cookie):
    url = "{}/configNew/dialogue/add".format(DM_IP_NEW)
    data = {
        "name": name,
        "description": description,
        "workspaceId": workspace_id,
        "versionId": version_id,
    }
    logPredix = "[对话-新平台][添加对话]{} data={}".format(url, data)
    Logger.info(logPredix)
    response = request_util.post(url, data, cookie)
    Logger.info(response.json())
    return response.json()["result"]


# 新平台-更新对话的描述详情
def updateDialogue(dialogue_id, description, workspace_id, version_id, cookie):
    url = "{}/configNew/dialogue/updateDescription".format(DM_IP_NEW)
    data = {
            "id": dialogue_id,
            "description": description,
            "workspaceId": workspace_id,
            "versionId": version_id,
        }
    logPredix = "[对话-新平台][更新对话的描述详情]{} data={}".format(url, data)
    Logger.info(logPredix)
    response = request_util.post(url, data, cookie)
    Logger.info(response.json())


# 新平台-添加意图和对话关系
def addRelationShipIntentAndDialogue(dialogue_id, intend_id, workspace_id, version_id, cookie):
    url = "{}/configNew/dialogueAccess/add".format(DM_IP_NEW)
    data = {
        "dialogueId": dialogue_id,
        "accessType": 'INTENT',
        "accessId": intend_id,
        "workspaceId": workspace_id,
        "versionId": version_id,
    }
    logPredix = "[对话-新平台][添加意图和对话关系]{} data={}".format(url, data)
    Logger.info(logPredix)
    response = request_util.post(url, data, cookie)
    Logger.info(response.json())
