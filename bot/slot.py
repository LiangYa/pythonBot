import json

from bot.dialogue import getDialogueList, getDialogueFromOld
from util import request_util
from config.settings import DM_IP_NEW, DM_IP_OLD

# 添加对话
from util.merge_cell_util import getPlaceStr


def addSlot(slot_info, workspace_id, version_id, dialogue_id, cookie):
    fillSlotActionVO = slot_info["fillSlotActionVO"]
    if fillSlotActionVO is not None:
        fillSlotActionVO["id"] = None
        interfaceParamTemplate = fillSlotActionVO["interfaceParamTemplate"]
        if interfaceParamTemplate is not None:
            interfaceParamTemplate["interfaceId"] = 21041
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
    # print("添加槽位"+str(data))
    url = "{}/configNew/slot/save".format(DM_IP_NEW)
    response = request_util.post_json(url, data, cookie)
    print(response.json())
    return response.json()["result"]


def getSlotFromOld(workspace_id, slot_id, cookie):
    url = "{}/config/slot/get?slotId={}&workspaceId={}".format(DM_IP_OLD, slot_id, workspace_id)
    response = request_util.get_old(url, cookie)
    json = response.json()
    print(json)
    return json["result"]


# 从老平台获取流程
def getFlowFromOld(workspace_id, dialogue_id, cookie):
    url = "{}/config/flow/init?workspaceId={}&dialogueId={}".format(DM_IP_OLD, workspace_id, dialogue_id)
    response = request_util.get(url, cookie)
    json = response.json()
    print(json)
    return json["result"]


def copyByDialogueId(old_workspace_id, old_dialogue_id, old_cookie,
                     workspace_id, version_id, dialogue_id, cookie):
    flowOldRes = getFlowFromOld(old_workspace_id, old_dialogue_id, old_cookie)
    flowOldJson = json.loads(flowOldRes["flow"])
    print(flowOldJson)
    nodeDataArray = flowOldJson["nodeDataArray"]
    for data in nodeDataArray:
        if int(data["id"]) > 0:
            if str(data["text"]) == "结果":
                if str(data["type"]) == "JUMP_DIALOGUE" or str(data["type"]) == "RETURN_DIALOGUE":
                    data["id"] = -1
                else:
                    # 添加结束
                    finalAct = getFinalActByOld(data["id"], old_workspace_id, old_cookie)
                    reply = finalAct["reply"]
                    if reply is not None:
                        reply = str(reply)
                    newFinalAct = setFinalAct(finalAct["actionTargetSystem"], reply, workspace_id, version_id, dialogue_id, cookie)
                    data["id"] = newFinalAct["id"]
            else:
                # 添加单个槽位
                slotInfo = getSlotFromOld(old_workspace_id, data["id"], old_cookie)
                slot = addSlot(slotInfo, workspace_id, version_id, dialogue_id, cookie)
                data["id"] = slot["slot"]["id"]
    commit(json.dumps(flowOldJson), workspace_id, version_id, dialogue_id, cookie)
    pass


# 提交到新平台
def commit(flow_old_json, workspace_id, version_id, dialogue_id, cookie, json=None):
    url = "{}/configNew/flow/commit".format(DM_IP_NEW)
    # datas = json.dumps(flowOldJson)
    data = {
        "workspaceId": workspace_id,
        "versionId": version_id,
        "dialogueId": dialogue_id,
        "flow": flow_old_json,
        "saveStateTrack": False
    }
    response = request_util.post(url, data, cookie)
    json = response.json()
    print(json)
    # return json["result"]


# 结束节点创建
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
    response = request_util.post_json(url, data, cookie)
    print(response.json())
    return response.json()["result"]


# 结束节点获取信息从老平台
def getFinalActByOld(action_id, workspace_id, old_cookie):
    url = "{}/config/flow/getFinalAct?actionId={}&workspaceId={}".format(DM_IP_OLD, action_id, workspace_id)
    response = request_util.get(url, old_cookie)
    json = response.json()
    print(json)
    return json["result"]

# 关系
def copyAllByDialogueList(old_workspace_id, old_cookie,
                     workspace_id, version_id, cookie):
    dialogueList = getDialogueList(workspace_id, version_id, cookie)
    oldDialogueList = getDialogueFromOld(old_workspace_id, old_cookie)
    relationList = []
    for dialogue in dialogueList:
        for old in oldDialogueList:
            if dialogue["name"] == old["name"]:
                relationCh = {}
                relationCh["id"] = dialogue["id"]
                relationCh["name"] = dialogue["name"]
                relationCh["old_id"] = old["id"]
                relationList.append(relationCh)
                break
    for i in range(0, len(relationList)):
        relation = relationList[i]
        print(str(relation["id"])+"**"+str(relation["name"])+"**"+str(relation["old_id"]))
        copyByDialogueId(old_workspace_id, relation["old_id"], old_cookie, workspace_id, version_id, relation["id"], cookie)
    print(relationList)
    return relationList


if __name__ == '__main__':
    old_cookie = "JSESSIONID=node0o18vvg9789yl1es91tb4goot05387624.node0"
    cookie = "JSESSIONID=node016trjbz5jwi251dc0g8sypdafi12.node0"
    # # 添加单个槽位
    # slotInfo = getSlotFromOld(345, 15095, old_cookie)
    # slot = addSlot(slotInfo, 15467, 15468, 18519, cookie)
    # relation = copyAllByDialogueList(350, old_cookie, 20717, 23487, cookie)
    print("***********")
    # print(relation)
    copyByDialogueId(347, 2012, old_cookie, 26913, 26914, 26488, cookie)

