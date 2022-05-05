from config.settings import DM_IP_NEW, DM_IP_OLD, DM_IP_OLD_TWO
from util import request_util
from util.logger import Logger


# 从新平台获取接口列表
def getInterfaceList(workspace_id, cookie):
    url = "{}/configNew/interface/list?workspaceId={}".format(DM_IP_NEW, workspace_id)
    logPredix = "[接口-新平台][新平台接口列表]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get(url, cookie)
    json = response.json()
    Logger.info(json)
    return json["result"]


# 新增接口信息
def addInterface(name, path_url, interface_desc, method, parameter_content, result_type, workspace_id, cookie):
    url = "{}/configNew/interface/updateOrSave".format(DM_IP_NEW)
    logPredix = "[接口-新平台][新增新平台接口]{}".format(url)
    Logger.info(logPredix)
    data = {
        "name": name,
        "url": path_url,
        "interfaceDesc": interface_desc,
        "method": method,
        "parameterContent": parameter_content,
        "resultType": result_type,
        "workspaceId": workspace_id
    }
    response = request_util.post(url, data, cookie)
    Logger.info(response.json())
    pass


# 从新平台获取接口列表
def getInterfaceListOld(workspace_id, cookie):
    url = "{}/config/interface/list?workspaceId={}&query=".format(DM_IP_OLD, workspace_id)
    logPredix = "[接口-旧平台][新平台接口列表]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get(url, cookie)
    res = response.json()
    Logger.info(res)
    return res["result"]


# 从旧平台获取接口列表
def getInterfaceListOldTwo(workspace_id, cookie):
    url = "{}/config/interface/list?workspaceId={}&query=".format(DM_IP_OLD_TWO, workspace_id)
    logPredix = "[接口-旧平台][新平台接口列表]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get(url, cookie)
    res = response.json()
    Logger.info(res)
    return res["result"]
