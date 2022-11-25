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
    cookie = "JSESSIONID=node01h0tse3lppqmy6iziuetrk2b84623442.node0"
    name = "返回主流程"
    # dialogue = createDialogueAndIntent(74690, 520877, name, cookie)
    # updateDialogueAndDesc(680383, 620922, cookie)
    dialogue = createDialogueAndIntent(586840, 399835, name, cookie)
    # dialogue = createDialogueAndIntent(661490, 661491, name, cookie)
    # Logger.info(dialogue)
