from service import interface_service, intent_service, dialogue_service, slot_service
from util.logger import Logger
from config.settings import DM_IP_NEW, DM_IP_OLD
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


def copyWorkOld(entityId, optionValue, synonym, workspaceId, cookie):
    url = "{}/config/entity/optionValue/add".format(DM_IP_OLD)
    data = {
        "entityId": entityId,
        "optionValue": optionValue,
        "synonym": synonym,
        "workspaceId": workspaceId,
    }
    response = request_util.post(url, data, cookie)
    print(response.json())


if __name__ == '__main__':
    old_cookie = 'JSESSIONID=node0npuz2rx0pnta1fr89ecyyoy6j9628381.node0'
    cookie = 'sidebar_toggle_state=off; JSESSIONID=node01uxfsbmj4ov08a8iygb5lnyeo1909374.node0'
    # copyWorkspace(187, old_cookie, 291166, 447371, cookie)
    copyWork(958112, "肯定态度",
"了解;有印象;知道;有医保;都有;清楚;我有;浏览过;听说过;介绍一下;说一下;你介绍;在听;方便;说话;明白;听过;有意向;听到;看到;关注;打开了;打开微信了;说吧;你说吧;你说;同意;确认;有社保;我也是;好像有;买了;缴过;有保险;记得;记着;买过;都有的;有过;之前有;都买着;在买;肯定有;肯定有的;交了;交完了;在你那办的;也有;有做过;这个有;交的有;那个有;满意;看过;应该是;应该有;好像是;这有;理解;领过;有这个;交的了;有买;有那个;有很多;现在有;听清;收到;有点印象;有吧;过来了;听得到;晓得;能听懂;听懂了;你讲;完成了;点开了;完事了;看见了;在，;在。;还在，;还在。;看了;有京东;砖吧，;转吧。;好的"
, 307079, 898372, cookie)
    copyWork(958112, "无态度", "我没有花钱;没听明白;能不能;是不是;好不好;有没有;明白不;有事没有", 307079, 898372, cookie)
    copyWork(958112, "否定态度",  "不了解;不太了解;没印象;没有印象;忘了;忘记;忘掉;不知道;没有医保;没医保;不清楚;我没有;没了解;不是很了解;挂了;没得;算了;没看过;没浏览过;再见;拜拜;挂掉;没听说过;你别介绍;不方便;记不清;不明白;没有意向;没听到;不同意;不是很清楚;不懂;不怎么清楚;没缴过;记不得;记不住;没买过;没有过;之前没有;肯定没有;也没有;没做过;没有做过;不太清楚;不满意;不记得;不太记得;不怎么记得;没有买;没看过;没记得;没有记得;不太有印象;没太有印象;不理解;没钱;买不起;没领过;没有这个;没有买;没有那个;没听清;没收到;没过来;听不到;不晓得;不太关注;没看到;没有看到;没用过;没用"
, 307079, 898372, cookie)

    # copyWorkOld(915754, "肯定态度",
    #             "看到;找到;你说;你讲;知道;方便;发送;了解;有印象;知道;有医保;都有;我有;浏览过;听说过;介绍一下;说一下;你介绍;在听;方便;说话;明白;听过;有意向;听到;关注;好了;打开了;继续说;同意;确认;申请过;清楚;好像有;用过",
    #          360, cookie)
    # copyWorkOld(915754, "无态度", "", 360, cookie)
    # copyWorkOld(915754, "否定态度",
    #             "没有找到;不了解;没有了解;不知道;没看到;不方便;别发;不了解;没印象;没有印象;忘了;忘掉;忘记;不是很了解;没了解;挂了;没得;算了;不太了解;没有医保;不知道;我没有;没浏览过;不太清楚;再见;拜拜;挂掉;没听说过;没有浏览过;你别介绍;不方便;记不清;不明白;没咋了解;没有意向;没听到;不同意;没申请过;不怎么清楚;不是很清楚;没有用过;没用过;没有申请过;不清楚",
    #          360, cookie)

    Logger.info("1234567")
    pass
