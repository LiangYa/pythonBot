import os

import requests
import xlrd as xlrd

from config.settings import DM_IP_NEW
from util.merge_cell_util import get_cell_type
from util.operate_excel import OperateExcel
from config.settings import DM_IP_OLD
from util import request_util


def dealFAQ():
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'excel/TM.xlsx')
    sheetFaq = readBook.sheet_by_name("FAQ")
    sheetWorkspaceList = []
    sheetVersionList = []
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    for i in range(1, 90):
        name = sheetFaq.cell(i, 0).value
        number = sheetFaq.cell(i, 2).value
        label = sheetFaq.cell(i, 3).value
        content = sheetFaq.cell(i, 4).value
        action = sheetFaq.cell(i, 6).value
        # actionLabel = sheetFaq.cell(i, 7).value
        # 处理faq名称和循环
        # name = name[0:str(name).find("\n")]
        answer = "[{}]@#{}||{}#@".format(label, number, content)
        # if actionLabel != '':
        #     answer = "[{}]".format(actionLabel) + answer
        if action == "挂机":
            answer = answer+"@@end@@@@notbreak@@"
        else:
            answer = answer+"@continue@"
        index = name.find("轮询")
        if index > 1:
            length = len(sheetVersionList)
            cell = sheetVersionList[length-1]
            oldAnswer = cell["答案"]
            answer = "#if($!FaqResult.standard_query_times == 1) {} #else {} #end".format(oldAnswer, answer)
            cell["答案"] = answer
            pass
        else:
            operateExcel.define_excel_format("默认分类", name, '', name, sheetWorkspaceList)
            operateExcel.define_excel_format("", name, '', answer, sheetVersionList)

    path = os.path.dirname(os.path.realpath(__file__)) + "/excel/FAQ_workspace1.xlsx"
    path2 = os.path.dirname(os.path.realpath(__file__)) + "/excel/FAQ_workspace2.xlsx"
    print(path)
    operateExcel.write_excel_info(sheetWorkspaceList, path)
    operateExcel.write_excel_info(sheetVersionList, path2)
    pass


def getInterfaceList(workspace_id, cookie):
    url = "{}/configNew/interface/list?workspaceId={}".format(DM_IP_NEW, workspace_id)
    headers = {
        'Cookie': cookie,
        'Host': '39.99.244.42:18631',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    response = requests.get(url, timeout=5, headers = headers)
    json = response.json()
    print(json)
    return json["result"]


def addInterface(name, path_url, interface_desc, method, parameter_content, result_type, workspace_id, cookie):
    url = "{}/configNew/interface/updateOrSave".format(DM_IP_NEW)
    headers = {
        'Cookie': cookie,
        'Host': '39.99.244.42:18631',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    data = {
        "name": name,
        "url": path_url,
        "interfaceDesc": interface_desc,
        "method": method,
        "parameterContent": parameter_content,
        "resultType": result_type,
        "workspaceId": workspace_id
    }
    response = requests.post(url=url, data=data, headers=headers)
    pass


# 更新接口
def updateInterfaceByHttp():
    cookie = 'JSESSIONID=node08q4uldaornp01nxxdr984gliq133147.node0'
    interfaceList = getInterfaceList(15164, cookie)
    for one in interfaceList:
        addInterface(one["name"], one["url"], one["interfaceDesc"], one["method"], one["parameterContent"],
                     one["resultType"], 15467, cookie)
    pass


def flowContent():
    readBook = xlrd.open_workbook(r'excel/BOT.xlsx')
    sheetContent = readBook.sheet_by_index(0)
    nrows = sheetContent.nrows
    for i in range(3, nrows):
        text = get_cell_type(i, 4)
        name = sheetContent.cell(i, 4).value
        qlabel = sheetContent.cell(i, 8).value
        content = sheetContent.cell(i, 9).value
        label = sheetContent.cell(i, 10).value
        print(name)

    pass


def saveContent(old_id, query_answer, workspace_id, old_cookie):
    url = "{}kb/qa/updateQueryAnswerById".format(DM_IP_OLD)
    data = {
        "id": old_id,
        "queryAnswer": query_answer,
        "workspaceId": workspace_id
    }
    response = request_util.post(url, data, old_cookie)
    json = response.json()
    # print(json)
    return json["result"]


def dealFAQ_JK():
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'excel/JK.xlsx')
    sheetFaq = readBook.sheet_by_name("FAQ")
    sheetWorkspaceList = []
    sheetVersionList = []
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    for i in range(1, 15):
        name = sheetFaq.cell(i, 0).value
        number = sheetFaq.cell(i, 2).value
        label = sheetFaq.cell(i, 3).value
        content = sheetFaq.cell(i, 4).value
        action = sheetFaq.cell(i, 6).value
        # actionLabel = sheetFaq.cell(i, 7).value
        # 处理faq名称和循环
        # name = name[0:str(name).find("\n")]
        answer = "[{}]@#{}||{}#@".format(label, number, content)
        # if actionLabel != '':
        #     answer = "[{}]".format(actionLabel) + answer
        if action == "挂机":
            answer = answer+"@@end@@@@notbreak@@"
        else:
            answer = answer+"@continue@【@@highIntention@@】"
            answer = "#if($!{slot.share_company.value.allHighInterestVersion} == 1)" + answer \
                     + "#else @continue@【@@highIntention@@】#end"
        index = name.find("轮询")
        if index > 1:
            length = len(sheetVersionList)
            cell = sheetVersionList[length-1]
            oldAnswer = cell["答案"]
            answer = "#if($!FaqResult.standard_query_times == 1) {} #else {} #end".format(oldAnswer, answer)
            cell["答案"] = answer
            pass
        else:
            operateExcel.define_excel_format("默认分类", name, '', name, sheetWorkspaceList)
            operateExcel.define_excel_format("", name, '', answer, sheetVersionList)
    saveContent(old_id, query_name, workspace_id, old_cookie)
    # path = os.path.dirname(os.path.realpath(__file__)) + "/excel/FAQ_workspace1.xlsx"
    path2 = os.path.dirname(os.path.realpath(__file__)) + "/excel/FAQ_workspace3.xlsx"
    # print(path)
    # operateExcel.write_excel_info(sheetWorkspaceList, path)
    operateExcel.write_excelinfo(sheetVersionList, path2)
    pass


if __name__ == '__main__':
    # 生成faq文件
    dealFAQ()
    # dealFAQ_JK()
    # 更新接口
    # updateInterfaceByHttp()
    # flowContent()
    pass