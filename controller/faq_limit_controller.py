# 统计一天  防误抢话 只有 isTry=True
def getDialogueController():
    listStr = ''
    with open("../excel/222", 'r') as f:
        lineStrList = f.readlines()
        for i in range(0, len(lineStrList)):
            num = lineStrList[i]
            listStr = "{},{}'".format(listStr, num.replace("\n", ""))
            # print(num)

    # print(result)
    print(str(listStr))


if __name__ == '__main__':
    getDialogueController()
    pass
