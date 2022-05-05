import os

import xlrd

from util.merge_cell_util import get_cell_type
from util.operate_excel import OperateExcel


def dealWorkspace():
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'../excel/京东策略-22年3月.xlsx')
    sheetFaq = readBook.sheet_by_index(0)
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    for i in range(239, 241):
        label2 = sheetFaq.cell(i, 4).value
        attitude = sheetFaq.cell(i, 6).value
        number = sheetFaq.cell(i, 8).value
        label = sheetFaq.cell(i, 10).value
        content = sheetFaq.cell(i, 9).value
        action = sheetFaq.cell(i, 12).value
        merged = sheetFaq.merged_cells
        label2 = get_cell_type(i, 4, merged, sheetFaq)
        print(attitude)
        answer = ""
        if number != '':
            number = str(number).replace("1C", "$!{slot.share_company.value.round}C")
            answer = "@#{}||{}#@".format(number, content)
            if label2 != '':
                answer = "[{}]".format(label2) + answer
            if label != '':
                answer = "[{}]".format(label) + answer
            if action == "挂机":
                answer = answer + "@@end@@@@notbreak@@"
        else:
            # string = ""
            # if attitude == "肯定":
            #     string = "#if(${session.queryAttitude} == \"是\") \n"
            # elif attitude == "否定":
            #     string  = "#elseif(${session.queryAttitude} == \"否\")\n"
            # elif attitude == "其他":
            #     string = "#else(${session.queryAttitude} == \"无\")"
            answer = "@continue@"
            if label2 != '':
                answer = "[{}]".format(label2) + answer
            if label != '':
                answer = "[{}]".format(label) + answer
        print(answer)
    pass


if __name__ == '__main__':
    dealWorkspace()