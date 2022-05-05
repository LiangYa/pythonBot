import xlrd

from util.merge_cell_util import get_cell_type
from service.import_file_service import importFileService


def printDialogueNew(start_index, end_index, filename):
    readBook = xlrd.open_workbook(r'../excel/{}'.format(filename))
    sheetFaq = readBook.sheet_by_index(0)
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    for i in range(start_index-1, end_index):
        attitude = sheetFaq.cell(i, 6).value
        number = sheetFaq.cell(i, 7).value
        label = sheetFaq.cell(i, 9).value
        content = sheetFaq.cell(i, 8).value
        action = sheetFaq.cell(i, 11).value
        merged = sheetFaq.merged_cells
        label2 = get_cell_type(i, 4, merged, sheetFaq)
        # name1 = get_cell_type(i, 1, merged, sheetFaq)
        impFileService = importFileService()
        if "FAQ" in attitude:
            string = '#if("$!FaqResult.a" != "") \n'
            print(string)
        elif "肯定" in attitude:
            string = "#if(${session.queryAttitude} == \"是\") \n"
            print(string)
        elif attitude == "否定":
            string = "#elseif(${session.queryAttitude} == \"否\")\n"
            print(string)
        elif attitude == "其他":
            string = "#elseif(${session.queryAttitude} == \"无\")\n"
            print(string)
        answer = impFileService.buildAnswerInfo(number, content, label, label2, action)
        print(i)
        print(answer)
    pass


if __name__ == '__main__':
    printDialogueNew(50, 53, "加微新BOT设计.xlsx")
