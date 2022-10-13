from config.settings import DM_IP_NEW
from util import request_util
from util.logger import Logger


class entityDao(object):
    def __init__(self, cookie):
        self.cookie = cookie
        self.log = Logger

    def getEntityList(self, workspace_id):
        # url = "{}/configNew/entity/list?type=NORMAL&workspaceId={}&versionId={}&query="\
        #     .format(DM_IP_NEW, workspace_id, version_id)
        url = "{}/configNew/entity/list?type=NORMAL&workspaceId={}&query="\
            .format(DM_IP_NEW, workspace_id)
        logPredix = "[实体-新平台][实体列表]{}".format(url)
        Logger.info(logPredix)
        response = request_util.get(url, self.cookie)
        Logger.info(response.json())
        return response.json()["result"]

    def addEntity(self, workspace_id, name):
        url = "{}/configNew/entity/add".format(DM_IP_NEW)
        logPredix = "[实体-新平台][实体列表]{}".format(url)
        Logger.info(logPredix)
        data = {
            "name": name,
            "workspaceId": workspace_id,
            "versionId": 0
        }
        response = request_util.post(url, data, self.cookie)
        Logger.info(response.json())
        return response.json()["result"]

    def addEntityValue(self, entityId, optionValue, synonym):
        url = "{}/configNew/entity/optionValue/add".format(DM_IP_NEW)
        data = {
            "entityId": entityId,
            "optionValue": optionValue,
            "synonym": synonym,
            "workspaceId": 0,
            "versionId": 0,
        }
        response = request_util.post(url, data, self.cookie)
        Logger.info(response.json())
        return response.json()["result"]

    def getEntityValueList(self, entityId):
        url = "{}/configNew/entity/optionValue/list?entityId={}&workspaceId=&versionId=&query="\
            .format(DM_IP_NEW, entityId)
        response = request_util.get(url, self.cookie)
        Logger.info(response.json())
        return response.json()["result"]