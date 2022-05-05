from service import slot_service


def copyWorkspace(old_workspace_id, old_cookie, workspace_id, version_id, cookie):
    # # 复制从新版本复制接口
    # interface_service.copyInterfaceByWorkspaceIdNew(15467, workspace_id, cookie)
    # 复制意图接口
    # intent_service.copyIntent(old_workspace_id, workspace_id, version_id, old_cookie, cookie)
    # 复制对话接口
    # dialogue_service.copyDialogue(workspace_id, version_id, cookie)
    # 复制单个对话接口
    slot_service.copyByDialogueId(old_workspace_id, 2222, old_cookie, workspace_id, version_id, 137150, cookie)
    # # 根据空间复制对话流程接口
    # slot_service.copyAllByDialogueList(old_workspace_id, old_cookie, workspace_id, version_id, cookie)


# 复制单个对话
def copyWorkspaceNew(ori_workspace_id, ori_version_id, ori_dialogue_id,
                     workspace_id, version_id, dialogue_id, cookie):
    slot_service.copyByDialogueIdNew(ori_workspace_id, ori_version_id, ori_dialogue_id,
                                     workspace_id, version_id, dialogue_id, cookie)


if __name__ == '__main__':
    old_cookie = 'JSESSIONID=node0rt3wpq1dmowi14e8j9qboynom234057.node0'
    cookie = 'sidebar_toggle_state=off; JSESSIONID=node01w8fu4ee4zw6f1fpdl2ue5wcj6114328.node0'
    copyWorkspace(324, old_cookie, 74915, 74916, cookie)



