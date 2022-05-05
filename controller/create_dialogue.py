from dao import intent_dao
from service import dialogue_service
from util.logger import Logger


def createDialogueAndIntent(workspace_id, version_id, name, cookie):
    # 创建意图接口
    intent = intent_dao.addIntent(name, name, workspace_id, version_id, cookie)
    # 创建对话接口
    dialogue = dialogue_service.createDialogue(workspace_id, version_id, name, intent["id"], cookie)
    return dialogue


# 主函数执行
if __name__ == '__main__':
    cookie = "JSESSIONID=node0gflqhr94ykth1weg2hy4c4lt1389980.node0"
    name = "测试-打断静音"
    dialogue = createDialogueAndIntent(46051, 46052, name, cookie)

    # dialogue = createDialogueAndIntent(50468, 104126, name, cookie)
    Logger.info(dialogue)
