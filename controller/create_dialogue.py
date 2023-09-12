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


# 创建对话
def createDialogueAndIntentOld(workspace_id, name, cookie):
    # 创建意图接口
    intent = intent_dao.addIntentOld(name, name, workspace_id, cookie)
    # 创建对话接口
    dialogue = dialogue_service.createDialogueOld(workspace_id, name, intent["id"], cookie)
    return dialogue


# 主函数执行
if __name__ == '__main__':
    cookie = "JSESSIONID=node019vzqo9jkkyma10n3hawo6ublo7448221.node0"
    name = "对话入口-家庭意外激活均分新规则-0908"
    # # dialogue = createDialogueAndIntent(74690, 520877, name, cookie)
    # 更新对话ID
    # updateDialogueAndDesc(55369, 1019111, cookie)

    dialogue = createDialogueAndIntent(55369, 1017062, name, cookie)

    # dialogue = createDialogueAndIntentOld(360, name, cookie)

    # # dialogue = createDialogueAndIntent(661490, 661491, name, cookie)
    # # Logger.info(dialogue)

    # title = "核身环节,子-核身-在忙,子-核身-人还是机器人,开场-环节,开场-在忙-无原因,开场-在忙-有原因,开产-额度多少,开产-费用问题,开场-不需要,开场-客户会考虑,主流程-是否有app,京东app操作流程,京东app操作流程-寻找借钱图标,京东金融app操作流程,京东金融app操作流程-寻找金条图标,通用引导激活流程-寻找评估额度图标,通用引激活款流程-完善信息人脸识别,通用引激活款流程-审核结果,通用引导借款流程-借款操作,通用引导借款流程-是否可以挂机自己操作,引导操作-在忙,引导操作-不需要,返回原流程"
    # title = "度小满公众号操作流程,度小满公众号操作流程-登录账号,度小满公众号操作流程-寻找立即入驻图标"
    # faqTitle = title.split(",")
    # for name in faqTitle:
    #     name = name.replace(" ", "")
    #     dialogue = createDialogueAndIntent(1157087, 1145024, name, cookie)
