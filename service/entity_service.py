from dao import entity_dao
from dao.entity_dao import entityDao
from util.logger import Logger


class entityService(object):
    def __init__(self, cookie):
        self.entity_dao = entityDao(cookie)
        self.log = Logger

    def getEntityList(self, workspace_id):
        entityList = self.entity_dao.getEntityList(workspace_id)
        # self.log.info(entityList)
        return entityList

    def addEntity(self, workspace_id, name):
        entity = self.entity_dao.addEntity(workspace_id, name)
        return entity

    def getEntityValueList(self, entity):
        entityList = self.entity_dao.getEntityValueList(entity)
        return entityList

    def addEntityValue(self, entityId, optionValue, synonym):
        entityValue = self.entity_dao.addEntityValue(entityId, optionValue, synonym)
        return entityValue


if __name__ == '__main__':
    cookie = "JSESSIONID=node01rsktqtj88rdn15st3ameph82f3234800.node0"
    entSer = entityService(cookie)
    listst = entSer.getEntityValueList(595164)
    print(listst)

