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
    cookie = 'sidebar_toggle_state=off; JSESSIONID=node01uhm1ql07na4n1avzlozxladrd34334.node0'

    # copyWorkspace(187, old_cookie, 291166, 447371, cookie)
    # ori_workspace_id = 680383
    # ori_version_id = 620922
    # ori_dialogue_id = 631661
    ori_workspace_id = 586840
    ori_version_id = 399835
    ori_dialogue_id = 456591

    workspace_id = 586840
    version_id = 399835
    dialogue_id = 276791

    copyWorkspaceNew(ori_workspace_id, ori_version_id, ori_dialogue_id
                     , workspace_id, version_id, dialogue_id, cookie)



