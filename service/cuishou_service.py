from config.settings import BASE_DIR


def getDee():
    path = "{}/excel/dialogueBreak-warn.log".format(BASE_DIR)
    print("PATH{}".format(path))
    strList = ""
    with open(path, 'r') as f:
        lineStrList = f.readlines()
        prlineStr = None
        for lineStr in lineStrList:
            if prlineStr != lineStr:
                if lineStr != '':
                    # if len(lineStr.split("-")) > 4:
                    strList = "{},'{}'".format(strList, lineStr.replace(" ", "").replace("\\n", ""))
                    # print(lineStr.split("-")[3])
            prlineStr = lineStr
    print(strList)


if __name__ == '__main__':
    getDee()
    pass
