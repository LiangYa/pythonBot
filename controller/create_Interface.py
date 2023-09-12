from service import interface_service


def copyInterfaceByWorkspaceId(workspace_id, cookie):
    # 复制从新版本复制接口
    interface_service.copyInterfaceByWorkspaceIdNew(661923, workspace_id, cookie)


# 主函数执行
if __name__ == '__main__':
    cookie = "JSESSIONID=node01j6nis1ixlyv6beygemm6jpa37080099.node0"
    copyInterfaceByWorkspaceId(1157087, cookie)
