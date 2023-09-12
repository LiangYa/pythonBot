import xlrd

from config import constants
from service.import_file_service import importFileService
from util.merge_cell_util import get_cell_type
from util.operate_excel import OperateExcel


def dealWorkspace(commUtil=None, impFileService=None):
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'../excel/星火保均分BOT.xlsx')
    # sheetFaq = readBook.sheet_by_index(1)
    sheetFaq = readBook.sheet_by_name("星火保均分NBS1call-0331")
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    impFileService = importFileService()
    for i in range(34, 35):
        attitude = sheetFaq.cell(i, 6).value
        number = sheetFaq.cell(i, 7).value
        label = sheetFaq.cell(i, 9).value
        content = sheetFaq.cell(i, 8).value
        action = sheetFaq.cell(i, 11).value
        merged = sheetFaq.merged_cells
        label2 = get_cell_type(i, 4, merged, sheetFaq)
        # name1 = get_cell_type(i, 1, merged, sheetFaq)
        # name = commUtil.creatName(attitude)
        answer = impFileService.buildAnswerInfo(number, content, label, label2, action)
        if number != '' and constants.ACTION_END not in action:
            # 1.2.1 添加判断跳过上一个节点
            answer = impFileService.jumpPreNode(answer, "分流_92")
        elif number != '' and constants.ACTION_END in action:
            if constants.ACTION_BREAK in action:
                answer = "{}{}".format(answer, constants.LABEL_BREAK_END)
                answer = impFileService.jumpPreNode(answer, "分流_48")
            else:
                answer = "{}{}".format(answer, constants.LABEL_END)
        else:
            answer = "{}{}".format(answer, constants.LABEL_CONTINUE)
        # print(i)
        print(answer)
    pass


def dealWorkspaceNew(start_index, end_index):
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'../excel/360借条加微-已、未结清现金红包.xlsx')
    # sheetFaq = readBook.sheet_by_index(0)
    sheetFaq = readBook.sheet_by_name("消费已结清现金回访-0601")
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    impFileService = importFileService()
    for i in range(start_index, end_index):
        number = sheetFaq.cell(i, constants.FLOW_RECORD_NUMBER).value
        label = sheetFaq.cell(i, constants.FLOW_LABEL_USER).value
        content = sheetFaq.cell(i, constants.FLOW_WORDS).value
        action = sheetFaq.cell(i, constants.FLOW_LABEL_ACTION).value
        merged = sheetFaq.merged_cells
        label2 = get_cell_type(i, constants.FLOW_LABEL_NODE, merged, sheetFaq)
        # name1 = get_cell_type(i, 1, merged, sheetFaq)
        # name = commUtil.creatName(attitude)
        answer = impFileService.buildAnswerInfo(number, content,
                                                str(label).replace(" ", ""),
                                                str(label2).replace("\t", ""), action)
        if number != '' and constants.ACTION_END not in action:
            # 1.2.1 添加判断跳过上一个节点
            answer = impFileService.jumpPreNode(answer, "分流_91")
        elif number != '' and constants.ACTION_END in action:
            if constants.ACTION_BREAK in action:
                answer = "{}{}".format(answer, constants.LABEL_BREAK_END)
                answer = impFileService.jumpPreNode(answer, "分流_91")
            else:
                answer = "{}{}".format(answer, constants.LABEL_END)
        else:
            answer = "{}{}".format(answer, constants.LABEL_CONTINUE)
        # print(i)
        print(answer)
    pass


if __name__ == '__main__':
    dealWorkspaceNew(71, 72)
    # dealWorkspace()
    # dealWork()
