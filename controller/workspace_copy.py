import pandas
import xlrd

from config import constants
from service.import_file_service import importFileService
from util.merge_cell_util import get_cell_type
from util.operate_excel import OperateExcel
import pandas as pd


def dealWorkspace11():
    df = pandas.read_excel(r'../excel/京东加微-22年4月.xlsx', sheet_name="全流程", header=0)
    df_list = df['录音编号'].unique()
    for jg in df_list:
        if jg == 'nan':
            continue
        print(jg)
    readBook = xlrd.open_workbook(r'../excel/京东加微-22年4月.xlsx')
    readBook.sheet_by_name()
    sheetFaq = readBook.sheet_by_index(5)
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    impFileService = importFileService()
    for i in range(138, 140):
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
            answer = impFileService.jumpPreNode(answer, "分流_45")
        elif number != '' and constants.ACTION_END in action:
            if constants.ACTION_BREAK in action:
                answer = "{}{}".format(answer, constants.LABEL_BREAK_END)
            else:
                answer = "{}{}".format(answer, constants.LABEL_END)
        else:
            answer = "{}{}".format(answer, constants.LABEL_CONTINUE)
        print(i)
        print(answer)
    pass


if __name__ == '__main__':
    dealWorkspace11()
