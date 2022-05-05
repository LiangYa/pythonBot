import json
from util.logger import Logger
from dao import slot_dao, dialogue_dao


# 从旧平台复制流程到新平台-单个复制
def copyByDialogueId(old_workspace_id, old_dialogue_id, old_cookie,
                     workspace_id, version_id, dialogue_id, cookie):
    Logger.info("[单个对话复制][从旧平台复制流程到新平台]{}到{}".format(old_dialogue_id, dialogue_id))
    flowOldRes = slot_dao.getFlowFromOld(old_workspace_id, old_dialogue_id, old_cookie)
    flowOldJson = json.loads(flowOldRes["flow"])
    # Logger.info(flowOldJson)
    nodeDataArray = flowOldJson["nodeDataArray"]
    for data in nodeDataArray:
        if int(data["id"]) > 0:
            if str(data["text"]) == "结果":
                if str(data["type"]) == "RETURN_DIALOGUE":
                    data["id"] = -1
                elif str(data["type"]) == "JUMP_DIALOGUE":
                    data["id"] = getJumpDialogueId(data["id"], old_workspace_id, old_cookie, workspace_id, version_id, cookie)
                else:
                    # 添加结束
                    finalAct = slot_dao.getFinalActByOld(data["id"], old_workspace_id, old_cookie)
                    reply = finalAct["reply"]
                    if reply is not None:
                        reply = str(reply)
                    newFinalAct = slot_dao.setFinalAct(finalAct["actionTargetSystem"], reply, workspace_id, version_id, dialogue_id, cookie)
                    data["id"] = newFinalAct["id"]
            else:
                # 添加单个槽位
                slotInfo = slot_dao.getSlotFromOld(old_workspace_id, data["id"], old_cookie)
                slot = slot_dao.addSlot(slotInfo, workspace_id, version_id, dialogue_id, cookie)
                data["id"] = slot["slot"]["id"]
    slot_dao.commit(json.dumps(flowOldJson), workspace_id, version_id, dialogue_id, cookie)


# 复制整个空间的对话流程
def copyAllByDialogueList(old_workspace_id, old_cookie, workspace_id, version_id, cookie):
    Logger.info("[多个对话复制][复制整个空间的对话流程]")
    relationList = getDialogueRelationship(old_workspace_id, old_cookie, workspace_id, version_id, cookie)
    for i in range(0, len(relationList)):
        relation = relationList[i]
        Logger.info(str(relation["id"])+"**"+str(relation["name"])+"**"+str(relation["old_id"]))
        copyByDialogueId(old_workspace_id, relation["old_id"], old_cookie, workspace_id, version_id, relation["id"], cookie)
    Logger.info(relationList)
    return relationList


# 获取新旧平台对话关系
def getDialogueRelationship(old_workspace_id, old_cookie, workspace_id, version_id, cookie):
    dialogueList = dialogue_dao.getDialogueList(workspace_id, version_id, cookie)
    oldDialogueList = dialogue_dao.getDialogueFromOld(old_workspace_id, old_cookie)
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
    return relationList


# 获取跳转对话的ID
def getJumpDialogueId(old_dialogue_id, old_workspace_id, old_cookie, workspace_id, version_id, cookie):
    relationList = getDialogueRelationship(old_workspace_id, old_cookie, workspace_id, version_id, cookie)
    dialogue_id = -1
    for relation in relationList:
        old_id = str(relation["old_id"])
        if old_id == old_dialogue_id:
            dialogue_id = relation["id"]
            break
    return dialogue_id


# 从旧平台复制流程到旧平台-单个复制
def copyByDialogueIdOld(old_workspace_id, old_dialogue_id, old_cookie, workspace_id, dialogue_id, cookie):
    Logger.info("[单个对话复制][从旧平台复制流程到旧平台]{}到{}".format(old_dialogue_id, dialogue_id))
    flowOldRes = slot_dao.getFlowFromOld(old_workspace_id, old_dialogue_id, old_cookie)
    flowOldJson = json.loads(flowOldRes["flow"])
    # Logger.info(flowOldJson)
    nodeDataArray = flowOldJson["nodeDataArray"]
    for data in nodeDataArray:
        if int(data["id"]) > 0:
            if str(data["text"]) == "结果":
                if str(data["type"]) == "RETURN_DIALOGUE":
                    data["id"] = -1
                elif str(data["type"]) == "JUMP_DIALOGUE":
                    pass
                else:
                    # 添加结束
                    finalAct = slot_dao.getFinalActByOld(data["id"], old_workspace_id, old_cookie)
                    reply = finalAct["reply"]
                    if reply is not None:
                        reply = str(reply)
                    newFinalAct = slot_dao.setFinalActOld(finalAct["actionTargetSystem"], reply, workspace_id, cookie)
                    data["id"] = newFinalAct["id"]
            else:
                # 添加单个槽位
                slotInfo = slot_dao.getSlotFromOld(old_workspace_id, data["id"], old_cookie)
                slot = slot_dao.addSlotOld(slotInfo, workspace_id, dialogue_id, cookie)
                data["id"] = slot["slot"]["id"]
    slot_dao.commitOld(json.dumps(flowOldJson), workspace_id, dialogue_id, cookie)


# 从新平台复制流程到新平台-单个复制
def copyByDialogueIdNew(ori_workspace_id, ori_version_id, ori_dialogue_id,
                     workspace_id, version_id, dialogue_id, cookie):
    Logger.info("[单个对话复制][从新平台复制流程到新平台]{}到{}".format(ori_dialogue_id, dialogue_id))
    flowOldRes = slot_dao.getFlowFromNew(ori_workspace_id, ori_version_id, ori_dialogue_id, cookie)
    flowOldJson = json.loads(flowOldRes["flow"])
    # Logger.info(flowOldJson)
    nodeDataArray = flowOldJson["nodeDataArray"]
    for data in nodeDataArray:
        if int(data["id"]) > 0:
            if str(data["text"]) == "结果":
                if str(data["type"]) == "RETURN_DIALOGUE":
                    # data["id"] = -1
                    pass
                elif str(data["type"]) == "JUMP_DIALOGUE":
                    pass
                    # data["id"] = -1
                    # data["id"] = getJumpDialogueId(data["id"], old_workspace_id, old_cookie, workspace_id, version_id, cookie)
                else:
                    # 添加结束
                    finalAct = slot_dao.getFinalActByNew(data["id"], ori_workspace_id, ori_dialogue_id, ori_version_id, cookie)
                    reply = finalAct["reply"]
                    if reply is not None:
                        reply = str(reply)
                    newFinalAct = slot_dao.setFinalAct(finalAct["actionTargetSystem"], reply, workspace_id, version_id, dialogue_id, cookie)
                    data["id"] = newFinalAct["id"]
            else:
                # 添加单个槽位
                slotInfo = slot_dao.getSlotFromNew(ori_workspace_id, data["id"], ori_version_id, cookie)
                slot = slot_dao.addSlot(slotInfo, workspace_id, version_id, dialogue_id, cookie)
                data["id"] = slot["slot"]["id"]
    slot_dao.commit(json.dumps(flowOldJson), workspace_id, version_id, dialogue_id, cookie)
