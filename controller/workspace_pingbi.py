# 新平台-京东加微
import xlrd

from util.merge_cell_util import get_cell_type_copy
from util.operate_excel import OperateExcel


def dealFAQ():
    readBook = xlrd.open_workbook(r'../excel/京东加微-22年4月.xlsx')
    sheetFaq = readBook.sheet_by_index(5)
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    faqSet = set()
    result = ""
    for i in range(55, 56):
        merged = sheetFaq.merged_cells
        title = str(get_cell_type_copy(i, 13, merged, sheetFaq))
        title2 = str(get_cell_type_copy(i, 14, merged, sheetFaq))
        title = "{}{}".format(title, title2)
        title = title.replace("屏蔽标签：\n", "").replace("\n", ",").replace("【", "").replace("】", ",").replace(",,", ",")\
            .replace(" ", "")
        if title != "" and title != '':
            faqTitle = title.split(",")
            if len(faqTitle) > 0:
                for faq in faqTitle:
                    if faq == '':
                        continue
                    faqSet.add(faq)
        if len(faqSet) > 0:
            for faqSetTitle in faqSet:
                result = result + "," + faqSetTitle
        print(result[1:len(result)])


def dealFAQ1():
    title = "有人联系过,投诉,你怎么有我号码,别给我打电话了,怀疑平台,询问工号,对甲方品牌的反应,非本人操作,不符合办卡条件-年龄问题,不符合办卡条件,强烈拒绝"
    faq_title_list = title.split(",")
    faq_express = ""
    for faq in faq_title_list:
        faq_express = faq_express + ' $!{FaqResult.standard_query} == "' + faq + '" ||'
    if faq_express != "":
        faq_express = faq_express[0:len(faq_express)-2]
    express = "#if({}) 1 #end".format(faq_express)
    print(express)


if __name__ == '__main__':
    dealFAQ()
