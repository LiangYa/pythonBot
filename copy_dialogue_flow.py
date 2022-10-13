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
    slot_service.copyByDialogueId(old_workspace_id, 1179, old_cookie, workspace_id, version_id, 447541, cookie)
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
    old_cookie = 'JSESSIONID=node0npuz2rx0pnta1fr89ecyyoy6j9628381.node0'
    cookie = 'sidebar_toggle_state=off; JSESSIONID=node01whs8flvvfw401aat6kcljoyoj1148104.node0'
    # copyWorkspace(187, old_cookie, 291166, 447371, cookie)
    copyWork(656729, "肯定态度", "看到;找到;你说;你讲;知道;方便;发送;了解;有印象;知道;有医保;都有;我有;浏览过;听说过;介绍一下;说一下;你介绍;在听;方便;说话;明白;听过;有意向;听到;关注;好了;打开了;继续说;同意;确认;申请过;清楚;好像有;用过", 637620, 656789, cookie)
    copyWork(656729, "无态度", "我没有花钱;没听明白;能不能;是不是;好不好;有没有;明白不;有事没有", 637620, 656789, cookie)
    copyWork(656729, "否定态度", "不了解;不太了解;没印象;没有印象;忘了;忘记;忘掉;不知道;没有医保;没医保;不清楚;我没有;没了解;不是很了解;挂了;没得;算了;没看过;没浏览过;再见;拜拜;挂掉;没听说过;你别介绍;不方便;记不清;不明白;没有意向;没听到;不同意;不是很清楚;不懂;不怎么清楚;没缴过;记不得;记不住;没买过;没有过;之前没有;肯定没有;也没有;没做过;没有做过;不太清楚;不满意;不记得;不太记得;不怎么记得;没有买;没看过;没记得;没有记得;不太有印象;没太有印象;不理解;没钱;买不起;没领过;没有这个;没有买;没有那个;没听清;没收到;没过来;听不到;不晓得;不太关注;没看到;没有看到", 637620, 656789, cookie)
    # copyWork(81517, "否定态度", "没有了;没看到;没听到;没看见;没收到;没找到;找不到;没有看到;没有收到;没有找到;没有看见;没有了;没有听到", 47310, 47311, cookie)
    # copyWork(81517, "无态度", "",  47310, 47311, cookie)
    # copyWork(58900, "肯定态度", "说一下;我有;听一听;在听;我听着;快一点;你说",  50468, 50469, cookie)
    Logger.info("1234567")
    pass
