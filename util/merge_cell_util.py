# 获取表格中所有合并单元格位置，以列表形式返回 （起始行，结束行，起始列，结束列）
import xlrd


def flowContent():
    readBook = xlrd.open_workbook(r'../excel/BOT.xlsx')
    sheetContent = readBook.sheet_by_index(0)
    merged = sheetContent.merged_cells
    nrows = sheetContent.nrows
    result = []
    for i in range(6, nrows):
        name = get_cell_type(i, 4, merged, sheetContent)
        old_number = sheetContent.cell(i, 7).value
        number = sheetContent.cell(i, 8).value
        content = sheetContent.cell(i, 9).value
        label = sheetContent.cell(i, 10).value
        if old_number != '':
            num_label = {}
            num_label["old_number"] = "@#" + str(old_number)[0:-3]
            if name is not None and name != '':
                num_label["label"] = "[" + name + "]@#" + str(number)[0:-3]
            else:
                num_label["label"] = "@#" + str(number)[0:-3]
            result.append(num_label)
        # print(name)
    return result


def flowContent_fandeng():
    readBook = xlrd.open_workbook(r'../excel/樊登读书策略详情.xlsx')
    sheetFaq = readBook.sheet_by_index(0)
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    for i in range(68, 63):
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


def getPlaceStr(content):
    if content is not None:
        dict_str = flowContent()
        for temp in dict_str:
            # todo 可能会出现录音编号不唯一 D10-1, D10
            old_number = temp["old_number"]
            label = temp["label"]
            content = str(content).replace(str(old_number), str(label))
    return content


def getPlaceStr_fandeng(content):
    if content is not None:
        dict_str = flowContent()
        for temp in dict_str:
            # todo 可能会出现录音编号不唯一 D10-1, D10
            old_number = temp["old_number"]
            label = temp["label"]
            content = str(content).replace(str(old_number), str(label))
    return content


# 获取合并单元格内容
def get_cell_type(row_index, col_index, merged, sheet):
    """既能得到合并单元格也能得到普通单元格"""
    cell_value = None
    for (rlow, rhigh, clow, chigh) in merged:  # 遍历表格中所有合并单元格位置信息
        # print(rlow,rhigh,clow,chigh)
        if (row_index >= rlow and row_index < rhigh):  # 行坐标判断
            if (col_index >= clow and col_index < chigh):  # 列坐标判断
                # 如果满足条件，就把合并单元格第一个位置的值赋给其它合并单元格
                cell_value = sheet.cell_value(rlow, clow)
                # print('合并单元格')
                break  # 不符合条件跳出循环，防止覆盖
            else:
                # print('普通单元格')
                cell_value = sheet.cell_value(row_index, col_index)

        # else:  添加改行后只那一个单元格的内容5，0 会返回2个值普通单元格/合并单元格
        #     print('普通单元格')
        #     cell_value = sheet.cell_value(row_index, col_index)

    return cell_value


# 获取合并单元格内容
def get_cell_type_copy(row_index, col_index, merged, sheet):
    """既能得到合并单元格也能得到普通单元格"""
    cell_value = None
    for (rlow, rhigh, clow, chigh) in merged:  # 遍历表格中所有合并单元格位置信息
        # print(rlow,rhigh,clow,chigh)
        if (row_index >= rlow and row_index < rhigh):  # 行坐标判断
            if (col_index >= clow and col_index < chigh):  # 列坐标判断
                # 如果满足条件，就把合并单元格第一个位置的值赋给其它合并单元格
                cell_value = sheet.cell_value(rlow, clow)
                # print('合并单元格')
                break  # 不符合条件跳出循环，防止覆盖
            else:
                # print('普通单元格')
                cell_value = sheet.cell_value(row_index, col_index)
        # else:  添加改行后只那一个单元格的内容5，0 会返回2个值普通单元格/合并单元格
        #     print('普通单元格')
        #     cell_value = sheet.cell_value(row_index, col_index)
    if cell_value is None:
        cell_value = sheet.cell_value(row_index, col_index)

    return cell_value


# 直接输入单元格的坐标。来获取单元格内容
# print(get_cell_type(5, 0))

# # 利用循环输出某列的单元格内容
# for i in range(1, 9):
#     print(get_cell_type(i, 2))


if __name__ == '__main__':
    flowContent()
    pass
