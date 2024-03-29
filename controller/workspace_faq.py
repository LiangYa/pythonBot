import os
import xlrd

from config import constants
from util.merge_cell_util import get_cell_type, get_cell_type_copy
from util.operate_excel import OperateExcel
from service.import_file_service import importFileService


# 去重
def dealRepeat():
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'../excel/FAQ_workspace1.xlsx')
    sheetFaq = readBook.sheet_by_index(0)
    namestr = ""
    j = 0
    for i in range(0, 716):
        name = sheetFaq.cell(i, 0).value
        if name in namestr:
            continue
        else:
            namestr = "{}{}".format(namestr, name)
            j = j+1
    print(namestr)
    print(j)


# 新平台-京东加微
def dealFAQ():
    labelUtil = importFileService()
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'../excel/金条-拉新激活纯机-淑婷版-0905.xlsx')
    sheetFaq = readBook.sheet_by_name("FAQ")
    # sheetFaq = readBook.sheet_by_index(1)
    sheetWorkspaceList = []
    sheetVersionList = []
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    for i in range(1, 118):
        recordNumber = sheetFaq.cell(i, 1).value  # 录音编号
        userLabel = sheetFaq.cell(i, 2).value  # 用户标签
        sceneTalk = sheetFaq.cell(i, 3).value  # 场景话术
        scoreLabel = sheetFaq.cell(i, 4)  # 标签分值
        actionLabel = sheetFaq.cell(i, 5).value  # 动作标签
        merged = sheetFaq.merged_cells
        title = get_cell_type_copy(i, 0, merged, sheetFaq)
        # title = sheetFaq.cell(i, 0).value  # FAQ名称
        faqSort = ""  # 分类
        if ncols > 6:
            faqSort = sheetFaq.cell(i, 6).value  # 分类
        beizhu = None
        if ncols > constants.FLOW_WORDS:
            beizhu = sheetFaq.cell(i, constants.FLOW_WORDS).value  # 备注
        answer = ""
        if recordNumber != '':
            if userLabel != '':
                answer = "[{}]".format(userLabel)
            if sceneTalk != '':
                answer = "{}@#{}||{}#@".format(answer, recordNumber, sceneTalk)
            if constants.ACTION_ADD_WECHAT in actionLabel:
                answer = "[{}]{}".format(constants.LABEL_ADD_WECHAT, answer)

            if constants.ACTION_BREAK in actionLabel and constants.ACTION_END in actionLabel:
                answer = "{}{}".format(answer, constants.LABEL_BREAK_END)
            elif constants.ACTION_END in actionLabel:
                answer = "{}{}".format(answer, constants.LABEL_END)
            else:
                answer = "{}{}".format(answer, constants.LABEL_CONTINUE)
            if constants.ACTION_SEND_SMS in actionLabel:
                answer = "[{}]{}".format(constants.LABEL_SEND_SMS, answer)
            # 发短信
            if (constants.ACTION_SEND_SMS_COM in actionLabel or constants.LABEL_SEND_SMS_COM in actionLabel) \
                    and constants.ACTION_SEND_SMS_COM_M not in actionLabel:
                answer = "[{}]{}".format(constants.LABEL_SEND_SMS_COM, answer)
            # 添加FAQ分类
            if constants.SORT_COMPLAINT in faqSort:
                answer = "{}{}".format(answer, constants.FAQ_SORT_COMPLAINT)
            elif constants.SORT_COMMON in faqSort:
                answer = "{}{}".format(answer, constants.FAQ_SORT_COMMON)
            elif constants.SORT_QUERY in faqSort:
                answer = "{}{}".format(answer, constants.FAQ_SORT_QUERY)
            elif constants.SORT_HIGH in faqSort:
                answer = "{}{}".format(answer, constants.FAQ_SORT_HIGH)
            elif constants.SORT_MIDDLE in faqSort:
                answer = "{}{}".format(answer, constants.FAQ_SORT_MIDDLE)
            answer = "{}{}".format(labelUtil.add_sort_label(faqSort), answer)
            if beizhu and "转人成功不播报" in beizhu:
                answer = "[{}]{}".format("转人成功不播报", answer)
            # 电销标签
            answer = "{}{}".format(labelUtil.add_common_label(actionLabel), answer)
            # # 标签分值
            # if scoreLabel != '':
            #     answer = "[{}]{}".format(scoreLabel, answer)
        length = len(sheetVersionList)
        preFaq = None
        if length > 0:
            preFaq = sheetVersionList[length-1]
        if "轮询" in title or (preFaq is not None and title == preFaq["标准问"]):
            oldAnswer = preFaq["答案"]
            answer = "#if($!FaqResult.standard_query_times == 1)\n\t{}\n#else\n\t{}\n#end".format(oldAnswer, answer)
            preFaq["答案"] = answer
        else:
            operateExcel.define_excel_format("默认分类", title, '', title, sheetWorkspaceList)
            operateExcel.define_excel_format("", title, '', answer, sheetVersionList)
    # path = os.path.dirname(os.path.realpath(__file__)) + "../excel/FAQ_workspace1.xlsx"
    # path2 = os.path.dirname(os.path.realpath(__file__)) + "../excel/FAQ_workspace2.xlsx"
    path = "../excel/FAQ_workspace1.xlsx"
    path2 = "../excel/FAQ_workspace2.xlsx"
    print(path)
    print(path2)
    operateExcel.write_excel_info(sheetWorkspaceList, path)
    operateExcel.write_excel_info(sheetVersionList, path2)


def dealFAQNew(start_index, end_index):
    labelUtil = importFileService()
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'../excel/养老人机bot(2216空间).xlsx')
    sheetFaq = readBook.sheet_by_name("不同地域不同回复FAQ")
    # sheetFaq = readBook.sheet_by_index(3)
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    reply = ""
    labelV = '#elseif("$!{slot.share_city_name.value}"'
    for i in range(start_index, end_index):
        recordNumber = sheetFaq.cell(i, 1).value  # 录音编号
        userLabel = sheetFaq.cell(i, 2).value  # 用户标签
        sceneTalk = sheetFaq.cell(i, 3).value  # 场景话术
        actionLabel = sheetFaq.cell(i, 5).value  # 动作标签
        merged = sheetFaq.merged_cells
        title = get_cell_type_copy(i, 0, merged, sheetFaq)
        city = sheetFaq.cell(i, 6).value  # 城市名称
        faqSort = ""  # 分类
        if ncols > 6:
            faqSort = sheetFaq.cell(i, 6).value  # 分类
        answer = ""
        if recordNumber != '':
            if userLabel != '':
                answer = "[{}]".format(userLabel)
            if sceneTalk != '':
                answer = "{}@#{}||{}#@".format(answer, recordNumber, sceneTalk)
            if constants.ACTION_ADD_WECHAT in actionLabel:
                answer = "[{}]{}".format(constants.LABEL_ADD_WECHAT, answer)

            if constants.ACTION_BREAK in actionLabel and constants.ACTION_END in actionLabel:
                answer = "{}{}".format(answer, constants.LABEL_BREAK_END)
            elif constants.ACTION_END in actionLabel:
                answer = "{}{}".format(answer, constants.LABEL_END)
            else:
                answer = "{}{}".format(answer, constants.LABEL_CONTINUE)
            if constants.ACTION_SEND_SMS in actionLabel:
                answer = "[{}]{}".format(constants.LABEL_SEND_SMS, answer)
            # 发短信
            if constants.ACTION_SEND_SMS_COM in actionLabel or constants.LABEL_SEND_SMS_COM in actionLabel:
                answer = "[{}]{}".format(constants.LABEL_SEND_SMS_COM, answer)
            # 添加FAQ分类
            if constants.SORT_COMPLAINT in faqSort:
                answer = "{}{}".format(answer, constants.FAQ_SORT_COMPLAINT)
            elif constants.SORT_COMMON in faqSort:
                answer = "{}{}".format(answer, constants.FAQ_SORT_COMMON)
            elif constants.SORT_QUERY in faqSort:
                answer = "{}{}".format(answer, constants.FAQ_SORT_QUERY)
            elif constants.SORT_HIGH in faqSort:
                answer = "{}{}".format(answer, constants.FAQ_SORT_HIGH)
            elif constants.SORT_MIDDLE in faqSort:
                answer = "{}{}".format(answer, constants.FAQ_SORT_MIDDLE)
            # 电销标签
            answer = "{}{}".format(labelUtil.add_common_label(actionLabel), answer)
            answer = '{} == "{}")\n{}\n'.format(labelV, city, answer)
            reply = "{}{}".format(reply, answer)
    print(reply)


def commFAQ():
    faq = '#if("$!{slot.share_subbot.value}" == "") \ntwo\n #else \none\n #end'
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'../excel/FAQ_workspace2.xlsx')
    faqOne = readBook.sheet_by_index(0)
    readBook = xlrd.open_workbook(r'../excel/FAQ_workspace3.xlsx')
    faqTwo = readBook.sheet_by_index(0)
    sheetVersionList = []
    j = 1
    for i in range(1, 91):
        query_one = faqOne.cell(i, 1).value  # 标准问
        answer_one = faqOne.cell(i, 3).value  # 答案
        query_two = faqTwo.cell(j, 1).value  # 标准问
        answer_two = faqTwo.cell(j, 3).value  # 答案
        answer = ""
        if query_one == query_two:
            j = j + 1
            answer = faq.replace("two", answer_two).replace("one", answer_one)
        else:
            answer = faq.replace("two", "@continue@").replace("one", answer_one)
        operateExcel.define_excel_format("", query_one, '', answer, sheetVersionList)
    path2 = "../excel/FAQ_workspace5.xlsx"
    print(path2)
    operateExcel.write_excel_info(sheetVersionList, path2)


if __name__ == '__main__':
    dealFAQ()
    # dealFAQNew(97, 108)
    # commFAQ()
    # dealRepeat()
