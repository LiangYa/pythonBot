from service import interface_service


def copyInterfaceByWorkspaceId(workspace_id, cookie):
    # 复制从新版本复制接口
    interface_service.copyInterfaceByWorkspaceIdNew(15467, workspace_id, cookie)


# 主函数执行
if __name__ == '__main__':
    cookie = "JSESSIONID=node018srjpu2kwxm11ikflal8aevwc330973.node0"
    copyInterfaceByWorkspaceId(74915, cookie)
