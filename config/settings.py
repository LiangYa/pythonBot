from pathlib import Path

ONLINE = False

# 服务器
# DM_IP_NEW = "http://121.89.242.146:18631"
# if ONLINE is True:
#     DM_IP_NEW = "http://172.26.7.20:18631"
# 服务器
DM_IP_NEW = "http://39.99.244.42:18631"
if ONLINE is True:
    DM_IP_NEW = "http://172.26.7.20:18631"

DM_IP_OLD = "http://8.142.85.77:8630/"
if ONLINE is True:
    DM_IP_OLD = "http://172.26.2.56:8630/"

DM_IP_OLD_TWO = "http://8.142.25.111:18630/"
if ONLINE is True:
    DM_IP_OLD_TWO = "http://172.26.5.70:18630/"

SALE_XI_AI = "https://sale.xi-ai.com"
if ONLINE is True:
    SALE_XI_AI = "http://172.26.5.106"

SALE_XI_AI_TWO = "https://work.xi-ai.com"

RECORD_ROUND = "1C"
INDEX_START = 91
INDEX_END = 100
SHARE_NAME = "login"
# COOKIE = "JSESSIONID=node0y4nfzlc7qo8zelxb6qxi8gp4869131.node0"

BASE_DIR = Path(__file__).resolve().parent.parent
