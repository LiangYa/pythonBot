from dao import entity_dao
from dao.entity_dao import entityDao
from util.logger import Logger


class entityService(object):
    def __init__(self):
        self.entity_dao = entityDao()
        self.log = Logger

    def getEntityList(self, workspace_id, version_id):
        entityList = self.entity_dao.getEntityList(workspace_id, version_id)
        # self.log.info(entityList)
        return entityList


if __name__ == '__main__':
    entSer = entityService()
    entSer.getEntityList(50468, 73850)
