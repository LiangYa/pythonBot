# 新平台-京东加微
import xlrd

from config import constants
from service.import_file_service import importFileService
from util.merge_cell_util import get_cell_type_copy, get_cell_type
from util.operate_excel import OperateExcel
from util.comUtil import CommonUtil


def dealFAQ():
    # labelUtil = importFileService()
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'../excel/京东养老金开户bot.xlsx')
    sheetFaq = readBook.sheet_by_name("京东养老金带操作-0630")
    sheetVersionList = []
    faq_question = ""
    pre_question = ""
    pre_round = 1
    index_start = 2
    index_end = 58
    for i in range(index_start, index_end):
        reverseOrder = sheetFaq.cell(i, constants.FLOW_ORDER).value
        if reverseOrder == 1.0:
            reverseOrder = 1
        attitude = sheetFaq.cell(i, constants.FLOW_ATTITUDE).value
        # todo 命中FAQ 可以修改
        if '命中FAQ' in attitude:
            attitude = "什么平台"
        number = sheetFaq.cell(i, constants.FLOW_RECORD_NUMBER).value
        label = sheetFaq.cell(i, constants.FLOW_LABEL_USER).value
        content = sheetFaq.cell(i, constants.FLOW_WORDS).value
        action = sheetFaq.cell(i, constants.FLOW_LABEL_ACTION).value
        merged = sheetFaq.merged_cells
        label_node = get_cell_type(i, constants.FLOW_NAME, merged, sheetFaq)
        cur_round = len(str(reverseOrder).split("."))
        if pre_round != cur_round and pre_question != '':
            if faq_question == "":
                faq_question = pre_question.replace("/n", "")
            else:
                faq_question = "{},{}".format(faq_question, pre_question.replace("/n", ""))
            pre_round = cur_round
            pre_question = ""
        if reverseOrder == 1 and i == index_start:
            operateExcel.define_excel_format_test(label_node, attitude,
                                                  "", number, content, sheetVersionList)
            cur_question = ""
        elif reverseOrder == 1 and i != index_start:
            for version in sheetVersionList:
                if version["录音编号"] != '':
                    continue
                faq_content = version["场景话术"]
                faq_question = version["请求话术"]
                if label_node in faq_content and "｜" in faq_content and attitude in faq_content:
                    version["录音编号"] = number
                    faq_question = faq_question
                elif label_node in faq_content and "｜" in faq_content:
                    continue
                elif label_node in version["场景话术"]:
                    version["录音编号"] = number
                    faq_question = faq_question
        else:
            if number != '' and constants.ACTION_END not in action:
                pre_round = cur_round
                pre_question = attitude
            content_temp = attitude
            if faq_question != "":
                content_temp = "{},{}".format(faq_question, attitude)
            operateExcel.define_excel_format_test(label_node, attitude, content_temp,
                                                  number, content, sheetVersionList)
    path = "../excel/workspace_test.xlsx"
    print(path)
    operateExcel.write_excel_info(sheetVersionList, path)


if __name__ == '__main__':
    dealFAQ()
    pass
