# 从平台获取信息
from config.settings import SALE_XI_AI
from util import request_util
from util.logger import Logger


# 获取录音编号
def getRecordManageList(company_id, tts_model):
    data = None
    try:
        url = "{}/admin/soundRecording/getRecordManageList?companyId={}&ttsModel={}"\
            .format(SALE_XI_AI, company_id, tts_model)
        logPredix = "[平台][获取录音编号]{}".format(url)
        Logger.info(logPredix)
        response = request_util.get(url, None)
        res = response.json()
        data = res["data"]
    except Exception as ex:
        Logger.error(ex)
    return data


if __name__ == '__main__':
    dataList = getRecordManageList(2137, "ziyun")
    print(dataList)
    pass
