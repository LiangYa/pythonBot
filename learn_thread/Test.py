import json

from learn_thread.redis_pool import redis_ali_client


def buildDataFromData(workspace_id):
    workspaceAndSlotInfo = {}
    # 1.获取规则
    # 从redis获取数据
    break_rules = redis_ali_client.get_redis_conn().get("breakRule_workspaceId:{}".format(workspace_id))
    if break_rules is None:
        # 从接口获取
        break_rules = ""
    if break_rules is not None:
        break_rules = json.loads(break_rules)
        slotRuleList = break_rules["slotRule"]
        for slotRule in slotRuleList:
            if "@@break@@" == str(slotRule["instructIntent"]["instruct"]):
                intentList = slotRule["instructIntent"]["intent"].split(",")
                intentSet = set()
                for intent in intentList:
                    intentSet.add(intent)
                workspaceAndSlotInfo[str(slotRule["slotId"])] = {
                    "instructIntentBreak": set(intentList)
                }
                if "什么平台"  in intentSet:
                    print(123)
    # if break_rules != {}
    # 从接口中获取数据
    return workspaceAndSlotInfo


if __name__ == '__main__':
    # query = "什么平台"
    # dm_replay = "《槽位id:46137》d1233dd4ddd5ddddddddddddddd"
    # predict(46051, "", dm_replay, query)
    workspaceAndSlotInfo = buildDataFromData(46051)
    print(workspaceAndSlotInfo)
