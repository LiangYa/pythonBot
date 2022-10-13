import re

from util.logger import reload_log
from util.merge_cell_util import get_cell_type

NAME_NUMBER = 0


class CommonUtil:
    def __init__(self):
        self.log = reload_log()
        pass

    # 获取新的名称
    def creatName(self, name):
        global NAME_NUMBER
        nameNew = name
        if name is not None and len(name) > 6:
            nameNew = name[0:6]
        nameNew = "{}{}".format(nameNew, str(NAME_NUMBER))
        NAME_NUMBER = NAME_NUMBER + 1
        return nameNew

    # 从返回的数据中解析出来
    def get_dialogue_name(self, contextStr):
        # pattern = r'【(\w+)|(\w+-)?】'
        contextStr = contextStr.replace("｜", "|")
        contextList = contextStr.split("|")
        context = contextList[0]
        pattern = r'【(.*)】'
        res = None
        # 去掉 【FAQ答案】
        context = context.replace("【FAQ答案】", "").replace("【faq答案】", "")
        matchRes = re.search(pattern, context)
        if matchRes is not None:
            res = matchRes.group(1)
        if "转成功" in context:
            res = "实时转接"
        self.log.info("从机器人话术中获取跳转对话:{}".format(res))
        return res


if __name__ == '__main__':
    ww = CommonUtil()
    ww.get_dialogue_name("【主-开场】｜【开场-表明来意首句】")
    pass

