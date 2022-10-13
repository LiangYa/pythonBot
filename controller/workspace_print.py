import xlrd

from config import constants
from service.import_file_service import importFileService
from util.merge_cell_util import get_cell_type
from util.operate_excel import OperateExcel


def dealWorkspace(commUtil=None, impFileService=None):
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'../excel/MT-美团发卡预测试bot.xlsx')
    sheetFaq = readBook.sheet_by_index(0)
    # sheetFaq = readBook.sheet_by_name("减免A-1call-白条")
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    impFileService = importFileService()
    for i in range(7, 8):
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


def dealWorkspaceRound(index_start, index_end):
    operateExcel = OperateExcel()
    readBook = xlrd.open_workbook(r'../excel/美团加微-22年5月.xlsx')
    sheetFaq = readBook.sheet_by_index(0)
    # sheetFaq = readBook.sheet_by_name("新版轮询-5.10")
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    impFileService = importFileService()
    roundStr = ""
    for i in range(index_start-1, index_end):
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
        if number != '' and "FAQ轮询" in attitude:
            att_num = str(attitude).replace("FAQ轮询", "")
            if "1" in att_num:
                roundStr = "#if({} && {} == {})\n\t{}".format('"$!FaqResult.a" != ""', "${globalVisitTime}", att_num, answer)
            else:
                roundStr = "{}\n#elseif({} && {} == {})\n\t{}".format(roundStr, '"$!FaqResult.a" != ""', "${globalVisitTime}", att_num, answer)
        elif number != '' and "静音轮询" in attitude:
            roundStr = "#if({} == 1)\n\t{}".format("${globalVisitTime}", answer)
        elif number != '' and constants.ACTION_END not in action:
            # 1.2.1 添加判断跳过上一个节点
            answer = impFileService.jumpPreNode(answer, "分流_32")
        elif number != '' and constants.ACTION_END in action:
            if constants.ACTION_BREAK in action:
                answer = "{}{}".format(answer, constants.LABEL_BREAK_END)
            else:
                answer = "{}{}".format(answer, constants.LABEL_END)
        else:
            answer = "{}{}".format(answer, constants.LABEL_CONTINUE)
        # print(i)
        if answer != '':
            print(answer)
            pass
    roundStr = "{}\n#else\n\t@continue@\n#end".format(roundStr)
    print(roundStr)
    pass


def dealWork():
    readBook = xlrd.open_workbook(r'../excel/20220826210421.xlsx')
    sheetFaq = readBook.sheet_by_index(0)
    eenen = ''
    num = 0
    for i in range(1, 19155):
        attitude = sheetFaq.cell(i, 0).value
        if "京东(无感)" in attitude:
            eenen = "{},{}".format(eenen, int(sheetFaq.cell(i, 1).value))
            num = num + 1
    print(eenen)
    print(num)


if __name__ == '__main__':
    # dealWorkspaceRound(223, 223)
    dealWorkspace()
    # dealWork()
