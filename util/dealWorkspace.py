import os

import xlrd

from util.operate_excel import OperateExcel


def dealWorkspace():
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'../excel/樊登读书策略详情.xlsx')
    sheetFaq = readBook.sheet_by_index(3)
    sheetWorkspaceList = []
    sheetVersionList = []
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    for i in range(104, 105):
        attitude = sheetFaq.cell(i, 5).value
        number = sheetFaq.cell(i, 6).value
        label = sheetFaq.cell(i, 7).value
        content = sheetFaq.cell(i, 10).value
        action = sheetFaq.cell(i, 12).value
        answer = ""
        if number != '':
            number = str(number).replace("1C", "$!{slot.share_company.value.round}C")
            answer = "[{}]@#{}||{}#@".format(label, number, content)
            if label == '':
                answer = "@#{}||{}#@".format(number, content)
            if action == "挂机":
                answer = answer + "@@end@@@@notbreak@@"
        else:
            string = ""
            if attitude == "肯定":
                string = "#if(${session.queryAttitude} == \"是\") \n"
            elif attitude == "否定":
                string = "#elseif(${session.queryAttitude} == \"否\")\n"
            elif attitude == "其他":
                string = "#else \n"
            answer = "[{}]@continue@".format(label)
            answer = string + answer + " \n#end"
        print(i)
        print(answer)
    pass


if __name__ == '__main__':
    dealWorkspace()
