from config.settings import BASE_DIR


# 统计一天  防误抢话 只有 isTry=True
def getDialogueController():
    path = "../logs/access-2022-08-16.log".format(BASE_DIR)
    print("PATH{}".format(path))
    result = []
    num = 0
    listStr = set()
    listNum = {
        "4872": 0,
        "295": 0,
        "299": 0,
        "291166": 0,
        "8660": 0,
        "345775": 0
    }
    with open(path, 'r') as f:
        lineStrList = f.readlines()
        for i in range(0, len(lineStrList)):
            lineStr = lineStrList[i]
            if lineStr != '' and "&isTry=False" in lineStr and "/dialogue/process" in lineStr:
                num = num + 1
            if lineStr != '' and "&isTry=True" in lineStr and "/dialogue/process" in lineStr:
                sessionId = lineStr.split("sessionId=")[1]
                query = str(sessionId).split("&query=")
                sessionId = query[0]
                workspaceId = str(query[1]).split("&workspaceId=")
                query = workspaceId[0]
                j = len(lineStrList) if i > len(lineStrList) else i + 1
                limitLen = len(lineStrList) if i+100 > len(lineStrList) else i+100
                for j in range(j, limitLen):
                    toLine = lineStrList[j]
                    if toLine == "" or ("/dialogue/process" not in toLine and "/dialogue/handleMissRecord" not in toLine):
                        continue
                    if "&isTry=False" in toLine and "/dialogue/process" in toLine and query in toLine:
                        break
                    elif query in toLine and sessionId in toLine and "/dialogue/handleMissRecord" in toLine:
                        result.append(toLine)
                        workspaceId = str(workspaceId[1]).split("&userId")[0]
                        listStr.add(workspaceId)
                        listSum = listNum.get(workspaceId, 0)
                        listNum[workspaceId] = int(listSum) + 1
                        if workspaceId == "8660":
                            print("{}".format(sessionId))
                    else:
                        # print(toLine)
                        pass

    with open("{}/logs/dialogueBreak.log".format(BASE_DIR), 'w') as f:
        for temp in result:
            f.write("{}\n".format(temp))
    # print(result)
    print(len(result))
    print(num)
    print(str(listStr))
    print(str(listNum))


if __name__ == '__main__':
    # getDialogueController()
    # sum = 767 + 49175
    # print("precent:{:.2%}".format(767/sum))
    # stringLen = "我不管你对我我我我不管你对我生活有影响还是什么影响。"
    stringLen = "我不管"
    print(len(stringLen))
    pass
