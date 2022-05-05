from config.settings import DM_IP_NEW
from util import request_util
from util.logger import Logger


def addFaqLimit(node_type="SLOT", slot_id=None, handle_type="NO_HANDLE", limit_faq=None,
                workspace_id=None, version_id=None, cookie=None):
    url = "{}/syncNew/addLimit".format(DM_IP_NEW)
    logPredix = "[意图-新平台][添加意图]{}".format(url)
    Logger.info(logPredix)
    data = {
        "nodeType": node_type,
        "nodeId": slot_id,
        "handleType": handle_type,
        "limitIds": limit_faq,
        "limitFaqType": "STANDARD",
        "workspaceId": workspace_id,
        "versionId": version_id
    }
    response = request_util.post(url, data, cookie)
    Logger.info(response.json())
    return response.json()["result"]
