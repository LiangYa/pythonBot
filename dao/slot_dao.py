import json
import time

from util import request_util
from config.settings import DM_IP_NEW, DM_IP_OLD, DM_IP_OLD_TWO
from util.logger import Logger
from service import interface_service


# 新平台-创建槽位节点
from util.merge_cell_util import getPlaceStr


def addSlot(slot_info, workspace_id, version_id, dialogue_id, cookie):
    fillSlotActionVO = slot_info["fillSlotActionVO"]
    if fillSlotActionVO is not None:
        fillSlotActionVO["id"] = None
        interfaceParamTemplate = fillSlotActionVO["interfaceParamTemplate"]
        if interfaceParamTemplate is not None:
            # 获取接口id 只是默认槽位
            interfaceParamTemplate["interfaceId"] = interface_service.getInterfaceByName("槽位填充", workspace_id, cookie)
            interfaceParamTemplate["id"] = None
    slot = slot_info["slot"]
    slot["id"] = -1
    slot["dialogueId"] = dialogue_id
    slot["workspaceId"] = workspace_id
    slot["entityId"] = ""
    slotCard = slot_info["slotCard"]
    initReply = slot_info["initReply"]
    # todo 替换文件录音编号替换
    # initReply = getPlaceStr(initReply)
    if initReply is None:
        initReply = ''
    data = {
        "actionId": None,
        "edges": [],
        "entities": None,
        "fillSlotActionVO": fillSlotActionVO,
        "interfaces": None,
        "initReply": initReply,
        "invalidReply": "",
        "limitOption": None,
        "slot": slot,
        "slotCard": slotCard,
        "slotNode": None,
        "slotOptionValues": None,
        "verifySlotActionVO": None,
        "versionId": version_id,
        "workspaceId": workspace_id
    }
    url = "{}/configNew/slot/save".format(DM_IP_NEW)
    logPredix = "[槽位-新平台][添加槽位信息]{}".format(url)
    Logger.info(logPredix)
    Logger.info(data)
    response = request_util.post_json(url, data, cookie)
    Logger.info(response.json())
    return response.json()["result"]


# 新平台-提交到新平台
def commit(flow_old_json, workspace_id, version_id, dialogue_id, cookie):
    url = "{}/configNew/flow/commit".format(DM_IP_NEW)
    data = {
        "workspaceId": workspace_id,
        "versionId": version_id,
        "dialogueId": dialogue_id,
        "flow": flow_old_json,
        "saveStateTrack": True
    }
    logPredix = "[槽位-新平台][提交新平台commit]{}".format(url)
    Logger.info(logPredix)
    response = request_util.post(url, data, cookie)
    resultJson = response.json()
    # Logger.info(resultJson)


# 新平台-创建结束节点
def setFinalAct(action_target_system, reply, workspace_id, version_id, dialogue_id, cookie):
    # TODO 文本录音替换
    # reply = getPlaceStr(reply)
    data = {
        "actionTargetSystem": action_target_system,
        "dialogueId": dialogue_id,
        "id": -3,
        "reply": reply,
        "versionId": version_id,
        "workspaceId": workspace_id
    }
    url = "{}/configNew/flow/setFinalAct".format(DM_IP_NEW)
    logPredix = "[槽位-新平台][创建结束节点]{}".format(url)
    Logger.info(logPredix)
    response = request_util.post_json(url, data, cookie)
    resultJson = response.json()
    # Logger.info(resultJson)
    return resultJson["result"]


# 旧平台-从旧平台获取槽位信息
def getSlotFromOld(workspace_id, slot_id, old_cookie):
    url = "{}/config/slot/get?slotId={}&workspaceId={}".format(DM_IP_OLD, slot_id, workspace_id)
    logPredix = "[槽位-旧平台][获取旧平台信息]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get_old(url, old_cookie)
    resultJson = response.json()
    Logger.info(resultJson)
    return resultJson["result"]


# 旧平台-从老平台获取流程
def getFlowFromOld(workspace_id, dialogue_id, cookie):
    url = "{}/config/flow/init?workspaceId={}&dialogueId={}".format(DM_IP_OLD, workspace_id, dialogue_id)
    logPredix = "[槽位-旧平台][获取旧平台流程json]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get(url, cookie)
    resultJson = response.json()
    Logger.info(resultJson)
    return resultJson["result"]


# 旧平台-结束节点获取信息从老平台
def getFinalActByOld(action_id, workspace_id, old_cookie):
    url = "{}/config/flow/getFinalAct?actionId={}&workspaceId={}".format(DM_IP_OLD, action_id, workspace_id)
    logPredix = "[槽位-旧平台][结束节点获取信息从老平台]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get(url, old_cookie)
    resultJson = response.json()
    Logger.info(resultJson)
    return resultJson["result"]


# 旧平台-创建结束节点
def setFinalActOld(action_target_system, reply, workspace_id, cookie):
    # TODO 文本录音替换
    # reply = getPlaceStr(reply)
    data = {
        "actionTargetSystem": action_target_system,
        "id": -3,
        "reply": reply,
        "workspaceId": workspace_id
    }
    url = "{}/config/flow/setFinalAct".format(DM_IP_OLD_TWO)
    logPredix = "[槽位-旧平台][创建结束节点]{}".format(url)
    Logger.info(logPredix)
    response = request_util.post_json(url, data, cookie)
    resultJson = response.json()
    Logger.info(resultJson)
    return resultJson["result"]


# 旧平台-创建槽位节点
def addSlotOld(slot_info, workspace_id, dialogue_id, cookie):
    fillSlotActionVO = slot_info["fillSlotActionVO"]
    if fillSlotActionVO is not None:
        fillSlotActionVO["id"] = None
        interfaceParamTemplate = fillSlotActionVO["interfaceParamTemplate"]
        if interfaceParamTemplate is not None:
            # 获取接口id 只是默认槽位
            interfaceParamTemplate["interfaceId"] = interface_service.getInterfaceByNameOld("槽位填充", workspace_id, cookie)
            interfaceParamTemplate["id"] = None

    slot = slot_info["slot"]
    slot["id"] = -2
    slot["dialogueId"] = dialogue_id
    slot["workspaceId"] = workspace_id
    slot["entityId"] = ""
    slot["fillSlotActionId"] = None
    slotCard = slot_info["slotCard"]
    if slotCard is None:
        slotCard = {"cardId": 0,
                    "cardType": "TEXT",
                    "source": "",
                    "title": "",
                    "content": "",
                    "voiceBroadType": 1,
                    "voiceContent": "",
                    "telBroadType": 1,
                    "telContent": "",
                    "confirmButton": 2,
                    "cancelButton": 2,
                    "cardKeys": ""}
    initReply = slot_info["initReply"]
    # todo 替换文件录音编号替换
    # initReply = getPlaceStr(initReply)
    if initReply is None:
        initReply = ''
    data = {
        "actionId": None,
        "edges": [],
        "entities": None,
        "fillSlotActionVO": fillSlotActionVO,
        "interfaces": None,
        "initReply": initReply,
        "invalidReply": "",
        "limitOption": None,
        "slot": slot,
        "slotCard": slotCard,
        "slotNode": None,
        "slotOptionValues": None,
        "verifySlotActionVO": None,
        "workspaceId": workspace_id
    }
    url = "{}/config/slot/save".format(DM_IP_OLD_TWO)
    logPredix = "[槽位-旧平台][添加槽位信息]{}".format(url)
    Logger.info(logPredix)
    Logger.info(data)
    response = request_util.post_json(url, data, cookie)
    Logger.info(response.json())
    return response.json()["result"]


# 旧平台-提交到旧平台
def commitOld(flow_old_json, workspace_id, dialogue_id, cookie):
    url = "{}/config/flow/commit".format(DM_IP_OLD_TWO)
    data = {
        "workspaceId": workspace_id,
        "dialogueId": dialogue_id,
        "flow": flow_old_json,
        "saveStateTrack": True
    }
    logPredix = "[槽位-新平台][提交新平台commit]{}".format(url)
    Logger.info(logPredix)
    response = request_util.post(url, data, cookie)
    resultJson = response.json()
    Logger.info(resultJson)


# 新平台-新建
def createSlot(slot_info, init_reply, workspace_id, version_id, dialogue_id, cookie, repeated=False):
    fillSlotActionVO = None
    initReply = init_reply
    optional = True
    slot = {
        "dialogueId": dialogue_id,
        "versionId": version_id,
        "workspaceId": workspace_id,
        "id": -2,
        "identity": "",
        "inherit": False,
        "isUserInput": 1,
        "name": slot_info["text"],
        "optional": optional,
        "rule": None,
        "slotValueSource": "USER_INPUT"
    }
    slotCard = {
        "cancelButton": 2,
        "cardId": 0,
        "cardKeys": "",
        "cardType": "TEXT",
        "confirmButton": 2,
        "content": "",
        "source": "",
        "telBroadType": 1,
        "telContent": "",
        "title": "",
        "voiceBroadType": 1,
        "voiceContent": ""
    }
    if str(slot_info["text"]) == "记录开始" or "直接转人" in str(slot_info["text"]):
        fillSlotActionVO = {
            "actionTargetSystem": "BUSINESS_SYSTEM",
            "interfaceParamTemplate": {
                "interfaceId": interface_service.getInterfaceByName("槽位填充", workspace_id, cookie),
                "paramTemplates": "{}",
                "resultTemplate": "1",
                "versionId": version_id,
                "workspaceId": workspace_id
            }
        }
        slot["identity"] = "share_{}".format(int(time.time()))
        if "直接转人" in str(slot_info["text"]):
            slot["identity"] = "share_transfer_flag"
        slot["slotValueSource"] = "INTERFACE"
        slot["optional"] = False
    data = {
        "actionId": None,
        "fillSlotActionVO": fillSlotActionVO,
        "initReply": initReply,
        "repeated": repeated,
        "slot": slot,
        "slotCard": slotCard,
        "versionId": version_id,
        "workspaceId": workspace_id
    }
    url = "{}/configNew/slot/save".format(DM_IP_NEW)
    logPredix = "[槽位-新平台][添加槽位信息]{}".format(url)
    Logger.info(logPredix)
    Logger.info(data)
    response = request_util.post_json(url, data, cookie)
    # Logger.info(response.json())
    return response.json()["result"]


# 新平台-复制
def copySlot(slot_infos, workspace_id, version_id, dialogue_id, cookie):
    fillSlotActionVO = None
    fillSlotAction = slot_infos["fillSlotActionVO"]
    initReply = slot_infos["initReply"]
    slot_info = slot_infos["slot"]
    slot = {
        "dialogueId": dialogue_id,
        "versionId": version_id,
        "workspaceId": workspace_id,
        "id": -2,
        "identity": slot_info["identity"],
        "inherit": slot_info["inherit"],
        "isUserInput": 1,
        "name": slot_info["name"],
        "optional": slot_info["optional"],
        "rule": None,
        "slotValueSource": slot_info["slotValueSource"]
    }
    slotCard = {
        "cancelButton": 2,
        "cardId": 0,
        "cardKeys": "",
        "cardType": "TEXT",
        "confirmButton": 2,
        "content": "",
        "source": "",
        "telBroadType": 1,
        "telContent": "",
        "title": "",
        "voiceBroadType": 1,
        "voiceContent": ""
    }
    if fillSlotAction is not None:
        interfaceParamTemplate = fillSlotAction["interfaceParamTemplate"]
        paramTemplates = "{}"
        resultTemplate = "1"
        if interfaceParamTemplate is not None:
            paramTemplates = interfaceParamTemplate["paramTemplates"]
            resultTemplate = interfaceParamTemplate["resultTemplate"]
        fillSlotActionVO = {
            "actionTargetSystem": fillSlotAction["actionTargetSystem"],
            "interfaceParamTemplate": {
                "interfaceId": interface_service.getInterfaceByName(fillSlotAction["businessInterface"]["name"], workspace_id, cookie),
                "paramTemplates": paramTemplates,
                "resultTemplate": resultTemplate,
                "versionId": version_id,
                "workspaceId": workspace_id
            }
        }
    data = {
        "actionId": None,
        "fillSlotActionVO": fillSlotActionVO,
        "initReply": initReply,
        "repeated": False,
        "slot": slot,
        "slotCard": slotCard,
        "versionId": version_id,
        "workspaceId": workspace_id
    }
    url = "{}/configNew/slot/save".format(DM_IP_NEW)
    logPredix = "[槽位-新平台][添加槽位信息]{}".format(url)
    Logger.info(logPredix)
    Logger.info(data)
    response = request_util.post_json(url, data, cookie)
    return response.json()["result"]


# 旧平台-新建
def createSlotOld(slot_info, init_reply, workspace_id, dialogue_id, cookie):
    fillSlotActionVO = None
    initReply = init_reply
    optional = True
    slot = {
        "dialogueId": dialogue_id,
        "workspaceId": workspace_id,
        "id": -2,
        "identity": "",
        "inherit": False,
        "isUserInput": 1,
        "name": slot_info["text"],
        "optional": optional,
        "rule": None,
        "slotValueSource": "USER_INPUT"
    }
    slotCard = {
        "cancelButton": 2,
        "cardId": 0,
        "cardKeys": "",
        "cardType": "TEXT",
        "confirmButton": 2,
        "content": "",
        "source": "",
        "telBroadType": 1,
        "telContent": "",
        "title": "",
        "voiceBroadType": 1,
        "voiceContent": ""
    }
    if str(slot_info["text"]) == "记录开始":
        fillSlotActionVO = {
            "actionTargetSystem": "BUSINESS_SYSTEM",
            "interfaceParamTemplate": {
                "interfaceId": interface_service.getInterfaceByNameOldTwo("槽位填充", workspace_id, cookie),
                "paramTemplates": "{}",
                "resultTemplate": "1",
                "workspaceId": workspace_id
            }
        }
        slot["identity"] = "share_{}".format(int(time.time()))
        slot["slotValueSource"] = "INTERFACE"
        slot["optional"] = False
    data = {
        "actionId": None,
        "fillSlotActionVO": fillSlotActionVO,
        "initReply": initReply,
        "slot": slot,
        "slotCard": slotCard,
        "workspaceId": workspace_id
    }
    url = "{}/config/slot/save".format(DM_IP_OLD_TWO)
    logPredix = "[槽位-旧平台][添加槽位信息]{}".format(url)
    Logger.info(logPredix)
    Logger.info(data)
    response = request_util.post_json(url, data, cookie)
    Logger.info(response.json())
    return response.json()["result"]


# 新平台-从新平台获取流程
def getFlowFromNew(workspace_id, version_id, dialogue_id, cookie):
    url = "{}/configNew/flow/init?workspaceId={}&dialogueId={}&versionId={}"\
        .format(DM_IP_NEW, workspace_id, dialogue_id, version_id)
    logPredix = "[槽位-新平台][获取新平台流程json]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get(url, cookie)
    resultJson = response.json()
    Logger.info(resultJson)
    return resultJson["result"]


# 新平台-结束节点获取信息从新平台
def getFinalActByNew(action_id, workspace_id, dialogue_id, version_id, cookie):
    url = "{}/config/flow/getFinalAct?actionId={}&workspaceId={}&versionId={}"\
        .format(DM_IP_NEW, action_id, workspace_id, dialogue_id, version_id)
    logPredix = "[槽位-新平台][结束节点获取信息从新平台]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get(url, cookie)
    resultJson = response.json()
    Logger.info(resultJson)
    return resultJson["result"]


# 新平台-从新平台获取槽位信息
def getSlotFromNew(workspace_id, slot_id, version_id, cookie):
    url = "{}/configNew/slot/get?slotId={}&workspaceId={}&versionId={}"\
        .format(DM_IP_NEW, slot_id, workspace_id, version_id)
    logPredix = "[槽位-新平台][获取新平台信息]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get_old(url, cookie)
    resultJson = response.json()
    # Logger.info(resultJson)
    return resultJson["result"]
