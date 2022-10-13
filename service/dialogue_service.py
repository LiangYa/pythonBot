from dao import intent_dao, dialogue_dao
from util.comUtil import CommonUtil
from util.logger import Logger


# (通过意图创建对话列表)
def copyDialogue(workspace_id, version_id, cookie):
    intentList = intent_dao.getIntentList(workspace_id, version_id, cookie)
    for one in intentList:
        dialogue = dialogue_dao.addDialogue(one["name"], one["description"], workspace_id, version_id, cookie)
        dialogue_dao.updateDialogue(dialogue["id"], dialogue["id"], workspace_id, version_id, cookie)
        dialogue_dao.addRelationShipIntentAndDialogue(dialogue["id"], one["id"], workspace_id, version_id, cookie)


# (通过意图创建对话列表)
def createDialogue(workspace_id, version_id, dialogue_name, intent_id, cookie):
    dialogue = dialogue_dao.addDialogue(dialogue_name, dialogue_name, workspace_id, version_id, cookie)
    dialogue_dao.updateDialogue(dialogue["id"], dialogue["id"], workspace_id, version_id, cookie)
    dialogue_dao.addRelationShipIntentAndDialogue(dialogue["id"], intent_id, workspace_id, version_id, cookie)
    return dialogue


# 更新对话信息
def updateDialogueInfo(workspace_id, version_id, cookie):
    dialogueList = dialogue_dao.getDialogueList(workspace_id, version_id, cookie)
    for dialogue in dialogueList:
        if dialogue is None:
            continue
        dialogue_dao.updateDialogue(dialogue["id"], dialogue["id"], workspace_id, version_id, cookie)
        Logger.info("dialogue_id:{}, dialogue_name:{}".format(dialogue["id"], dialogue["name"]))


# 获取对话列表
def getDialogueNew(workspace_id, version_id, dialogue_name, cookie):
    dialogueList = dialogue_dao.getDialogueList(workspace_id, version_id, cookie)
    dialogue_id = -2
    for dialogue in dialogueList:
        if dialogue_name in dialogue["name"]:
            dialogue_id = "{}".format(dialogue["id"])
            Logger.info("dialogue_id:{}, dialogue_name:{}".format(dialogue["id"], dialogue["name"]))
            break
    return dialogue_id


def getAllDialogueIds(workspace_id, version_id, cookie):
    dialogueList = dialogue_dao.getDialogueList(workspace_id, version_id, cookie)
    ids = []
    for i in range(0, len(dialogueList)):
        ids.append(dialogueList[i]["id"])
    return ids


# 根据话术内容获取对话ID
def getDialogueIdByContext(workspace_id, version_id, context, cookie):
    util = CommonUtil()
    dialogue_name = util.get_dialogue_name(context)
    if dialogue_name is None:
        return -2
    dialogue_id = getDialogueNew(workspace_id, version_id, dialogue_name, cookie)
    return dialogue_id


# 根据话术内容获取跳转子流程
def getDialogueName(context):
    util = CommonUtil()
    dialogue_name = util.get_dialogue_name(context)
    if dialogue_name is None:
        return None
    return dialogue_name


if __name__ == '__main__':
    cookie = "JSESSIONID=node018srjpu2kwxm11ikflal8aevwc330973.node0"
    node_id = getDialogueIdByContext(74915, 74916, "【引导加微环节-挂机】|【常规首句】", cookie)
    print(node_id)
    pass