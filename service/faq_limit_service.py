
# 更新接口
from dao import faq_limit_dao


def addFaqLimit(node_type="SLOT", slot_id=None, handle_type="NO_HANDLE", limit_faq=None,
                workspace_id=None, version_id=None, cookie=None):
    faqLimitDao = faq_limit_dao.addFaqLimit(slot_id=slot_id, limit_faq=limit_faq,
                                            workspace_id=workspace_id, version_id=version_id,
                                            cookie=cookie)
