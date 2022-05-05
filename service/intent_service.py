from dao import intent_dao


# 更新接口
def copyIntent(old_workspace_id, workspace_id, version_id, old_cookie, cookie):
    intentList = intent_dao.getIntentFromOld(old_workspace_id, old_cookie)
    for one in intentList:
        intent_dao.addIntent(one["name"], one["description"], workspace_id, version_id, cookie)
    pass

