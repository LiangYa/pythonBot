from service import interface_service


def copyInterfaceByWorkspaceId(workspace_id, cookie):
    # 复制从新版本复制接口
    interface_service.copyInterfaceByWorkspaceIdNew(661923, workspace_id, cookie)


# 主函数执行
if __name__ == '__main__':
    cookie = "JSESSIONID=node01wylvjg2tu7d71xvwyfzke3yyu5532808.node0"
    copyInterfaceByWorkspaceId(586840, cookie)
