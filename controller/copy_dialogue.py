from service import slot_service


def copyWorkspace(old_workspace_id, old_cookie, workspace_id, version_id, cookie):
    # # 复制从新版本复制接口
    # interface_service.copyInterfaceByWorkspaceIdNew(15467, workspace_id, cookie)
    # 复制意图接口
    # intent_service.copyIntent(old_workspace_id, workspace_id, version_id, old_cookie, cookie)
    # 复制对话接口
    # dialogue_service.copyDialogue(workspace_id, version_id, cookie)
    # 复制单个对话接口
    slot_service.copyByDialogueId(old_workspace_id, 1476, old_cookie, workspace_id, version_id, 156777, cookie)
    # # 根据空间复制对话流程接口
    # slot_service.copyAllByDialogueList(old_workspace_id, old_cookie, workspace_id, version_id, cookie)


# 复制单个对话
def copyWorkspaceNew(ori_workspace_id, ori_version_id, ori_dialogue_id,
                     workspace_id, version_id, dialogue_id, cookie):
    slot_service.copyByDialogueIdNew(ori_workspace_id, ori_version_id, ori_dialogue_id,
                                     workspace_id, version_id, dialogue_id, cookie)


if __name__ == '__main__':
    old_cookie = ""
    cookie = 'sidebar_toggle_state=off; JSESSIONID=node0549e8rsbwidj1ad5lqy9pk8rq305826.node0'

    # copyWorkspace(358, cookie, 360, 447371, cookie)
    # ori_workspace_id = 680383
    # ori_version_id = 620922
    # ori_dialogue_id = 631661

    ori_workspace_id = 55369
    ori_version_id = 1017062
    ori_dialogue_id = 1092953

    workspace_id = 55369
    version_id = 1017062
    dialogue_id = 1207454

    copyWorkspaceNew(ori_workspace_id, ori_version_id, ori_dialogue_id
                     , workspace_id, version_id, dialogue_id, cookie)



