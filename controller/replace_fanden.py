import requests
import xlrd

from ReadFile import updateInterfaceByHttp, flowContent
from config.settings import DM_IP_OLD, DM_IP_NEW
from util import request_util


# faq内容标签修改
def getContent(filter_query, workspace_id, old_cookie):
    url = "{}kb/qa/listByQuery?pageNum=1&pageSize=10&workspaceId={}&filterQuery={}&qaTypeId=&query="\
        .format(DM_IP_OLD, workspace_id, filter_query)
    response = request_util.get(url, old_cookie)
    json = response.json()
    # print(json)
    return json["result"]


def saveContent(old_id, query_answer, workspace_id, old_cookie):
    url = "{}/kb/qa/updateQueryAnswerById".format(DM_IP_OLD)
    data = {
        "id": old_id,
        "queryAnswer": query_answer,
        "workspaceId": workspace_id
    }
    response = request_util.post(url, data, old_cookie)
    json = response.json()
    # print(json)
    return json["result"]


def getContent_new(filter_query, workspace_id, version_id, cookie):
    url = "{}/kbNew/qa/listByQuery?pageNum=1&pageSize=10&workspaceId={}&versionId={}&filterQuery={}&qaTypeId=&query="\
        .format(DM_IP_NEW, workspace_id, version_id, str(filter_query))
    response = request_util.get(url, cookie)
    json = response.json()
    return json["result"]


def saveContent_new(old_id, query_answer, workspace_id, version_id, cookie):
    url = "{}/kbNew/qa/updateQueryAnswerById".format(DM_IP_NEW)
    data = {
        "id": old_id,
        "queryAnswer": query_answer,
        "workspaceId": workspace_id,
        "versionId": version_id
    }
    response = request_util.post(url, data, cookie)
    json = response.json()
    return json["result"]


def replaceFAQ(workspace_id, old_cookie):
    readBook = xlrd.open_workbook(r'../excel/FAQ分层1.xlsx')
    sheetFaq = readBook.sheet_by_index(2)
    # 行
    nrows = sheetFaq.nrows
    high = 0
    mid = 0
    for i in range(1, nrows):
        label_name = sheetFaq.cell(i, 0).value
        label_intent = sheetFaq.cell(i, 1).value
        contentObject = getContent(label_name, workspace_id, old_cookie)
        if int(contentObject["totalCount"]):
            data = contentObject["data"]
            old_id = data[0]["id"]
            query_name = data[0]["queryAnswer"]
            workspace_id = data[0]["systemId"]
            if str(data) != "[]" and label_intent == '高':
                query_name = query_name + "【@@highIntention@@】"
                saveContent(old_id, query_name, workspace_id, old_cookie)
                print("{}".format(label_name))
            elif str(data) != "[]" and label_intent == '中':
                query_name = query_name + "【@@middleIntention@@】"
                print("{}".format(label_name))
                saveContent(old_id, query_name, workspace_id, old_cookie)
            elif str(data) != "[]" and label_intent == '分':
                mid = mid + 1
                query_name = str(query_name).replace("【@@middleIntention@@】", "").replace("【@@highIntention@@】", "")
                query_name = query_name + "【@@Layered@@】"
                print("{}".format(label_name))
                saveContent(old_id, query_name, workspace_id, old_cookie)
            else:
                query_name = str(query_name).replace("【@@middleIntention@@】", "").replace("【@@highIntention@@】", "")
                print("{}".format(label_name))
                saveContent(old_id, query_name, workspace_id, old_cookie)
    print("high:{}, mid:{}".format(high, mid))


def replaceFAQ_new(workspace_id, version_id, cookie):
    readBook = xlrd.open_workbook(r'../excel/FAQ分层1.xlsx')
    sheetFaq = readBook.sheet_by_index(2)
    # 行
    nrows = sheetFaq.nrows
    high = 0
    mid = 0
    for i in range(5, nrows):
        label_name = sheetFaq.cell(i, 0).value
        label_intent = sheetFaq.cell(i, 1).value
        contentObject = getContent_new(label_name, workspace_id, version_id, cookie)
        if int(contentObject["totalCount"]):
            data = contentObject["data"]
            old_id = data[0]["id"]
            query_name = data[0]["queryAnswer"]
            # workspace_id = data[0]["systemId"]
            if str(data) != "[]" and label_intent == '高':
                query_name = query_name + "【@@highIntention@@】"
                saveContent_new(old_id, query_name, workspace_id, version_id, cookie)
                print("{}".format(label_name))
            elif str(data) != "[]" and label_intent == '中':
                query_name = query_name + "【@@middleIntention@@】"
                print("{}".format(label_name))
                saveContent_new(old_id, query_name, workspace_id, version_id, cookie)
            elif str(data) != "[]" and label_intent == '分':
                query_name = str(query_name).replace("【@@middleIntention@@】", "").replace("【@@highIntention@@】", "")
                query_name = query_name + "【@@Layered@@】"
                print("{}".format(label_name))
                saveContent_new(old_id, query_name, workspace_id, version_id, cookie)
            else:
                query_name = str(query_name).replace("【@@middleIntention@@】", "").replace("【@@highIntention@@】", "")
                print("{}".format(label_name))
                saveContent_new(old_id, query_name, workspace_id, version_id, cookie)

    print("high:{}, mid:{}".format(high, mid))


def replaceFAQ_JK(old_cookie):
    readBook = xlrd.open_workbook(r'../excel/FAQ_workspace3.xlsx')
    sheetFaq = readBook.sheet_by_index(0)
    # 行
    nrows = sheetFaq.nrows
    high = 0
    mid = 0
    for i in range(1, nrows):
        label_name = sheetFaq.cell(i, 0).value
        label_intent = sheetFaq.cell(i, 1).value
        contentObject = getContent(label_name, old_cookie)
        data = contentObject["data"]
        if str(data) != "[]":
            old_id = data[0]["id"]
            query_name = data[0]["queryAnswer"]
            workspace_id = data[0]["systemId"]
            saveContent(old_id, label_intent, workspace_id, old_cookie)
            print("{}".format(label_name))
    print("high:{}, mid:{}".format(1, 2))


if __name__ == '__main__':
    old_cookie = 'JSESSIONID=node0g1o471yt9v1yf5auoyothnoc9377206.node0'
    replaceFAQ(350, old_cookie)
    # replaceFAQ_JK(old_cookie)
    # 更新接口
    # updateInterfaceByHttp()
    # flowContent()
    pass
