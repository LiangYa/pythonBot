import os
import xlrd

from config import constants
from util.merge_cell_util import get_cell_type, get_cell_type_copy
from util.operate_excel import OperateExcel
from service.import_file_service import importFileService


# 新平台-京东加微
def dealFAQ():
    labelUtil = importFileService()
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'../excel/MT-美团发卡预测试bot.xlsx')
    # sheetFaq = readBook.sheet_by_name("FAQ")
    sheetFaq = readBook.sheet_by_index(1)
    sheetWorkspaceList = []
    sheetVersionList = []
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    for i in range(1, 19):
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


if __name__ == '__main__':
    dealFAQ()
