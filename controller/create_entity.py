from service.entity_service import entityService


def copyEntityByWorkspaceId(old_workspace_id, target_workspace_id, cookie):
    entSer = entityService(cookie)
    entityList = entSer.getEntityList(old_workspace_id)
    if entityList is None or len(entityList) <= 0:
        return
    for entity in entityList:
        entityNew = entSer.addEntity(target_workspace_id, entity["name"])
        entityValueList = entSer.getEntityValueList(entity["id"])
        if entityValueList is None or len(entityValueList) <= 0:
            continue
        for entityValue in entityValueList:
            entSer.addEntityValue(entityNew["id"], entityValue["optionValue"], entityValue["synonym"])
        print(entity)
    print(entityList)


if __name__ == '__main__':
    cookie = "JSESSIONID=node019f07h6rog4m41dgvc5sgpzwy01427639.node0"
    # copyEntityByWorkspaceId(545632, 575712)
    copyEntityByWorkspaceId(545632, 1157087, cookie)
