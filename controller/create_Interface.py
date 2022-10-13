from service import interface_service


def copyInterfaceByWorkspaceId(workspace_id, cookie):
    # 复制从新版本复制接口
    interface_service.copyInterfaceByWorkspaceIdNew(47310, workspace_id, cookie)


# 主函数执行
if __name__ == '__main__':
    cookie = "JSESSIONID=node011qesp9arhtngy13cq1pwswv03688879.node0"
    copyInterfaceByWorkspaceId(661883, cookie)
