from dao.interface_dao import getInterfaceList, addInterface


# 复制新平台的接口列表
def copyInterfaceByWorkspaceIdNew(ordinary_workspace, target_workspace, cookie):

    interfaceList = getInterfaceList(ordinary_workspace, cookie)
    for one in interfaceList:
        addInterface(one["name"], one["url"], one["interfaceDesc"], one["method"], one["parameterContent"],
                     one["resultType"], target_workspace, cookie)
    pass
