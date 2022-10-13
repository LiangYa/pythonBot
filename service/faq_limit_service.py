
# 更新接口
from dao import faq_limit_dao
from service.dialogue_service import getAllDialogueIds


def addFaqLimit(workspace_id=None, version_id=None, node_type="SLOT",
                handle_type="NO_HANDLE", limit_faq=None, limitFaqType="STANDARD",
                limitType="faq", limitRule="exclud",  cookie=None):
    dialogueIds = getAllDialogueIds(workspace_id, version_id, cookie)
    dialogueIds.remove(107264)
    dialogueIds.remove(107372)
    # dialogueIds.remove(187631)
    for dialogueId in dialogueIds:
        faqRes = faq_limit_dao.getLimitList(version_id, dialogueId, "DIALOGUE", cookie)
        faq = limit_faq
        if faqRes is not None:
            faq = "{},{}".format(faqRes["limitIds"], faq)
        faqLimitDao = faq_limit_dao.addFaqLimit(node_type=node_type, slot_id=dialogueId, limit_faq=faq,
                                                workspace_id=workspace_id, version_id=version_id, cookie=cookie)
        pass



if __name__ == '__main__':
    cookie = "sidebar_toggle_state=off; JSESSIONID=node0l5awi44lq9rb1hi8xrflinf2540038.node0"
    faq = "领取条件,发劵方式"
    addFaqLimit(47310, 107228, "DIALOGUE", "NO_HANDLE", faq,
                "STANDARD", "faq", "exclud", cookie)
    pass

