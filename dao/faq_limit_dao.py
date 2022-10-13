from config.settings import DM_IP_NEW
from util import request_util
from util.logger import Logger


def addFaqLimit(node_type="SLOT", slot_id=None, handle_type="NO_HANDLE", limit_faq=None,
                workspace_id=None, version_id=None, cookie=None):
    url = "{}/syncNew/addLimit".format(DM_IP_NEW)
    logPredix = "[屏蔽-新平台][添加屏蔽]{}".format(url)
    Logger.info(logPredix)
    data = {
        "workspaceId": workspace_id,
        "versionId": version_id,
        "nodeType": node_type,
        "nodeId": slot_id,
        "handleType": handle_type,
        "limitIds": limit_faq,
        "limitFaqType": "STANDARD",
        "limitType": "faq",
        "limitRule": "exclude"
    }
    response = request_util.post(url, data, cookie)

    return response.json()["result"]


def getLimitList(version_id, slot_id, node_type, cookie):
    url = "{}/syncNew/getLimitList?versionId={}&nodeType={}&nodeId={}"\
        .format(DM_IP_NEW, version_id, node_type, slot_id)
    logPredix = "[屏蔽-新平台][查询屏蔽]{}".format(url)
    Logger.info(logPredix)
    response = request_util.get(url, cookie)
    return response.json()["result"]

