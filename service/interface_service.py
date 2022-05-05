from dao.interface_dao import getInterfaceList, addInterface, getInterfaceListOld, getInterfaceListOldTwo


# 复制新平台的接口列表
def copyInterfaceByWorkspaceIdNew(ordinary_workspace, target_workspace, cookie):
    interfaceList = getInterfaceList(ordinary_workspace, cookie)
    for one in interfaceList:
        addInterface(one["name"], one["url"], one["interfaceDesc"], one["method"], one["parameterContent"],
                     one["resultType"], target_workspace, cookie)
    pass


# 根据接口名获取接口ID
def getInterfaceByName(name, workspace_id, cookie):
    interfaceList = getInterfaceList(workspace_id, cookie)
    interfaceId = None
    for one in interfaceList:
        if one["name"] == name:
            interfaceId = one["id"]
    return interfaceId


# 根据接口名获取接口ID
def getInterfaceByNameOld(name, workspace_id, cookie):
    interfaceList = getInterfaceListOld(workspace_id, cookie)
    interfaceId = None
    for one in interfaceList:
        if one["name"] == name:
            interfaceId = one["id"]
            break
    return interfaceId


# 根据接口名获取接口ID
def getInterfaceByNameOldTwo(name, workspace_id, cookie):
    interfaceList = getInterfaceListOldTwo(workspace_id, cookie)
    interfaceId = None
    for one in interfaceList:
        if one["name"] == name:
            interfaceId = one["id"]
            break
    return interfaceId

