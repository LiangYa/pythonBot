import json
import re

import redis
from redis import Connection


class RedisAliClient(object):
    def __init__(self):
        pool = redis.ConnectionPool(host="dm-8vbhbqm1mjard4hw4epd.redis.zhangbei.rds.aliyuncs.com", port=6379, password="Lingxird12345!@#", decode_responses=True)
        # pool = redis.ConnectionPool(connection_class=conn, max_connections=10)
        # redis.ConnectionPool()
        self.conn_pool = redis.Redis(connection_pool=pool)

    def get_redis_conn(self):
        """
        get redis conn
        :return:
        """
        return self.conn_pool


redis_ali_client = RedisAliClient()

if __name__ == '__main__':
    # conn_pool = redis.Redis(host="dm-8vbhbqm1mjard4hw4epd.redis.zhangbei.rds.aliyuncs.com", port=6379,
    #                              password="Lingxird12345!@#")
    # string = conn_pool.get("simulator_993_1646811255260::1969")
    nn = {
        "workspaceRule":{
            "workspaceId":15467,
            "Instruct":1,
            "instructNumber":1,
            "instructTime":1,
            "instructIntent":{
                "instruct":"@@break@@",
                "intent":"什么平台,关于活动,人还是机器人"
            }
        },
        "slotRule": [
            {
                "slotId": 66825,
                "instructNumber": 1,
                "instructTime": 1,
                "instructIntent": {
                    "instruct": "@@break@@",
                    "intent": "什么平台,关于活动,人还是机器人"
                    # "intent":"什么平台,关于活动,人还是机器人"
                }
            },
            {
                "slotId": 66817,
                "instructNumber": 1,
                "instructTime": 1,
                "instructIntent": {
                    "instruct": "@@break@@",
                    "intent": "什么平台,关于活动"
                }
            }
        ]
    }

    # redis_ali_client.get_redis_conn().set('breakRule_workspaceId:993', json.dumps(nn), px=100)
    string = redis_ali_client.get_redis_conn().get("breakRule_workspaceId:{}".format(993))
    # dm_replay = "《槽位12id:46137》d1233dd4ddd5ddddddddddddddd"
    # pattern = r'《槽位id:(\d+)》'
    # slot_id = 1
    # pattern_slot = re.compile(pattern)
    # reslut = pattern_slot.findall(dm_replay)
    print(string)
    #
    # ee = re.search(pattern, dm_replay)
    # e = ee.group(1)
    # print(e < 1)


    # return slot_id
    # print(string)
