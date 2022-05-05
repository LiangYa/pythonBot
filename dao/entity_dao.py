from config.settings import DM_IP_NEW, COOKIE
from util import request_util
from util.logger import Logger


class entityDao(object):
    def getEntityList(self, workspace_id, version_id):
        url = "{}/configNew/entity/list?type=NORMAL&workspaceId={}&versionId={}&query="\
            .format(DM_IP_NEW, workspace_id, version_id)
        logPredix = "[实体-新平台][实体列表]{}".format(url)
        Logger.info(logPredix)
        response = request_util.get(url, COOKIE)
        Logger.info(response.json())
        return response.json()["result"]

    def addEntity(self, workspace_id, version_id, name):
        url = "{}/configNew/entity/add".format(DM_IP_NEW)
        logPredix = "[实体-新平台][实体列表]{}".format(url)
        Logger.info(logPredix)
        data = {
            "name": name,
            "workspaceId": workspace_id,
            "versionId": version_id
        }
        response = request_util.post_json(url, data, COOKIE)
        Logger.info(response.json())
        return response.json()["result"]

    def addEntityValue(self, entityId, optionValue, synonym, workspaceId, versionId):
        url = "{}/configNew/entity/optionValue/add".format(DM_IP_NEW)
        data = {
            "entityId": entityId,
            "optionValue": optionValue,
            "synonym": synonym,
            "workspaceId": workspaceId,
            "versionId": versionId,
        }
        response = request_util.post(url, data, COOKIE)
        Logger.info(response.json())
        return response.json()["result"]

