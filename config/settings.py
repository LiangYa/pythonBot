from pathlib import Path

ONLINE = False

# 服务器
DM_IP_NEW = "http://39.99.244.42:18631"
if ONLINE is True:
    DM_IP_NEW = "http://172.26.7.20:18631"

DM_IP_OLD = "http://8.142.85.77:8630/"
if ONLINE is True:
    DM_IP_OLD = "http://172.26.2.56:8630/"

DM_IP_OLD_TWO = "http://8.142.8.47:18630/"
if ONLINE is True:
    DM_IP_OLD_TWO = "http://172.26.5.70:18630/"

SALE_XI_AI = "https://sale.xi-ai.com"
if ONLINE is True:
    SALE_XI_AI = "http://172.26.5.106"

RECORD_ROUND = "1C"
INDEX_START = 2
INDEX_END = 14
SHARE_NAME = "not_understand"
COOKIE = "JSESSIONID=node0ouvmotqohseetkq93pxy9le2140657.node0"

BASE_DIR = Path(__file__).resolve().parent.parent
