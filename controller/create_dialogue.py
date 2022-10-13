from dao import intent_dao
from service import dialogue_service
from util.logger import Logger


# 创建对话
def createDialogueAndIntent(workspace_id, version_id, name, cookie):
    # 创建意图接口
    intent = intent_dao.addIntent(name, name, workspace_id, version_id, cookie)
    # 创建对话接口
    dialogue = dialogue_service.createDialogue(workspace_id, version_id, name, intent["id"], cookie)
    return dialogue


# 更新对话ID
def updateDialogueAndDesc(workspace_id, version_id, cookie):
    dialogue_service.updateDialogueInfo(workspace_id, version_id, cookie)


# 主函数执行
if __name__ == '__main__':
    cookie = "JSESSIONID=node0eph1qs77s8nm1mp6ckq7n0rh04075277.node0"
    name = "其他意图"
    # dialogue = createDialogueAndIntent(74690, 520877, name, cookie)
    # updateDialogueAndDesc(74690, 520877, cookie)
    dialogue = createDialogueAndIntent(345775, 101904, name, cookie)
    # Logger.info(dialogue)
