from service import interface_service, intent_service, dialogue_service, slot_service
from util.logger import Logger
from config.settings import DM_IP_NEW
from util import request_util


def copyWorkspace(old_workspace_id, old_cookie, workspace_id, version_id, cookie):
    # # 复制从新版本复制接口
    # interface_service.copyInterfaceByWorkspaceIdNew(15467, workspace_id, cookie)
    # 复制意图接口
    # intent_service.copyIntent(old_workspace_id, workspace_id, version_id, old_cookie, cookie)
    # 复制对话接口
    # dialogue_service.copyDialogue(workspace_id, version_id, cookie)
    # 复制单个对话接口
    slot_service.copyByDialogueId(old_workspace_id, 2228, old_cookie, workspace_id, version_id, 76042, cookie)
    # # 根据空间复制对话流程接口
    # slot_service.copyAllByDialogueList(old_workspace_id, old_cookie, workspace_id, version_id, cookie)


def copyWork(entityId, optionValue, synonym, workspaceId, versionId, cookie):
    url = "{}/configNew/entity/optionValue/add".format(DM_IP_NEW)
    data = {
        "entityId": entityId,
        "optionValue": optionValue,
        "synonym": synonym,
        "workspaceId": workspaceId,
        "versionId": versionId,
    }
    response = request_util.post(url, data, cookie)
    print(response.json())


if __name__ == '__main__':
    # old_cookie = 'JSESSIONID=node01c9bm8am4rfcw1xmxeww48xnwn2375885.node0'
    cookie = 'sidebar_toggle_state=off; JSESSIONID=node014jjw7k4dfeco74155ksojomi111902.node0'
    # copyWorkspace(345, old_cookie, 47310, 47311, cookie)
    copyWork(135810, "肯定态度", "有了;看到;听到;看见;收到;找到", 74855, 74856, cookie)
    # copyWork(81517, "否定态度", "没有了;没看到;没听到;没看见;没收到;没找到;找不到;没有看到;没有收到;没有找到;没有看见;没有了;没有听到", 47310, 47311, cookie)
    # copyWork(81517, "无态度", "",  47310, 47311, cookie)
    # copyWork(58900, "肯定态度", "说一下;我有;听一听;在听;我听着;快一点;你说",  50468, 50469, cookie)
    Logger.info("1234567")
    pass
