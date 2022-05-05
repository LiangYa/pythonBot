from service.entity_service import entityService


def copyEntityByWorkspaceId(workspace_id, version_id):
    entSer = entityService()
    entSer.getEntityList(workspace_id, version_id)


if __name__ == '__main__':
    copyEntityByWorkspaceId(50468, 73850)
