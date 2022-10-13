import json
import random
import time

import xlrd
from numpy.compat import long

import util
from config import constants
from config.settings import INDEX_START, INDEX_END, SHARE_NAME
from service.dialogue_service import getDialogueIdByContext, getDialogueName
from service.import_file_service import importFileService
from util.comUtil import CommonUtil
from util.logger import Logger
from util.merge_cell_util import get_cell_type
from dao import slot_dao


# Excel导入流程
# 京东-新平台创建对话流程
def createSlotsNew(workspace_id, version_id, cookie):
    readBook = xlrd.open_workbook(r'../excel/京东BOT.xlsx')
    sheetFaq = readBook.sheet_by_index(4)
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    nodeDataArray = [
        {
            "text": "开始",
            "id": -1,
            "figure": "RoundedRectangle",
            "type": "DIALOGUE",
            "parameter1": 100,
            "loc": "325 0",
            "key": -1
        },
        {
            "text": "记录开始",
            "id": -2,
            "figure": "RoundedRectangle",
            "type": "SLOT",
            "fill": "#FAD165",
            "parameter1": 100,
            "key": -2,
            "loc": "325 125"
        }
    ]
    linkDataArray = [
        {
            "from": -1,
            "to": -2,
            "text": "",
            "condition": {
                "compareType": "EQUALS"
            }
        }
    ]
    replyCollects = {
        -2: ""
    }
    # 读取Excel中的数据和构造节点
    pre_node_name = "记录开始"
    pre_node_key = -2
    next_node_name = ""
    next_node_key = None
    cur_node_key = -2
    dialogue_round = 1
    dialogue_branch = 0
    commUtil = CommonUtil()
    impFileService = importFileService()
    for i in range(INDEX_START, INDEX_END):
        # label2 = sheetFaq.cell(i, 4).value
        reverseOrder = sheetFaq.cell(i, 5).value
        if reverseOrder == 1.0:
            reverseOrder = 1
        attitude = sheetFaq.cell(i, 6).value
        number = sheetFaq.cell(i, 7).value
        label = sheetFaq.cell(i, 9).value
        content = sheetFaq.cell(i, 8).value
        action = sheetFaq.cell(i, 11).value
        merged = sheetFaq.merged_cells
        label2 = get_cell_type(i, 4, merged, sheetFaq)
        # name1 = get_cell_type(i, 1, merged, sheetFaq)
        name = commUtil.creatName(attitude)
        # 计算轮次
        cur_node_key = cur_node_key - 1
        cur_round = len(str(reverseOrder).split("."))
        if cur_round != dialogue_round and next_node_key is not None:
            pre_node_key = next_node_key
            pre_node_name = next_node_name
            next_node_key = None
            next_node_name = ""
            dialogue_branch = 1
            dialogue_round = cur_round
        else:
            dialogue_branch = dialogue_branch + 1
        answer = impFileService.buildAnswerInfo(number, content, label, label2, action)
        if number != '' and constants.ACTION_END not in action:
            # FAQ轮询1次拦截
            if "FAQ轮询1次" in attitude:
                answer = impFileService.jumpPreNodeTwoFAQ(answer, replyCollects, cur_node_key+1)
                continue
            # 1.槽位节点
            # 1.1创建下一个槽位
            if next_node_key is None:
                next_node_name = "分流_{}".format(random.randint(1, 100))
                next_node_key = cur_node_key
                nextData = addSlotNode(next_node_name, next_node_key, dialogue_branch, dialogue_round * 2 + 1)
                nodeDataArray.append(nextData)
                # reply_key = next_node_name + str(next_node_key)
                reply_key = next_node_key
                replyCollects[reply_key] = ""
                cur_node_key = cur_node_key - 1
            # 1.2创建当前槽位
            curData = addSlotNode(name, cur_node_key, dialogue_branch, dialogue_round * 2)
            nodeDataArray.append(curData)
            # reply_key = name + str(cur_node_key)
            reply_key = cur_node_key
            # 1.2.1 添加判断跳过上一个节点
            answer = impFileService.jumpPreNodeTwo(answer, pre_node_name)
            replyCollects[reply_key] = answer
            # 1.3建立关系-上一个节点和当前关系，当前节点和下一个节点关系
            curLink = addLinkData(pre_node_key, cur_node_key, name, attitude, dialogue_branch,
                                  dialogue_round=dialogue_round)
            nextLink = addLinkData(cur_node_key, next_node_key, "", "", 0)
            linkDataArray.append(curLink)
            linkDataArray.append(nextLink)
        elif number != '' and constants.ACTION_END in action:
            # 标签节点（扭转节点） + 结果节点
            if constants.ACTION_BREAK in action:
                answer = "{}{}".format(answer, constants.LABEL_BREAK_END)
            else:
                answer = "{}{}".format(answer, constants.LABEL_END)
            nodeDataEnd = addEndNode(k=cur_node_key, dialogue_branch=dialogue_branch, dialogue_round=dialogue_round * 2)
            nodeDataArray.append(nodeDataEnd)
            # reply_key = "结果"+str(cur_node_key)
            reply_key = cur_node_key
            replyCollects[reply_key] = answer
            curLink = addLinkData(pre_node_key, cur_node_key, name, attitude, dialogue_branch, dialogue_round)
            linkDataArray.append(curLink)
        elif answer == '':
            # 结果节点（跳转）
            node_id = long(getDialogueIdByContext(workspace_id, version_id, content, cookie))
            nodeDataEnd = addEndNode(cur_node_key, dialogue_branch, dialogue_round * 2, "JUMP_DIALOGUE", node_id)
            nodeDataArray.append(nodeDataEnd)
            curLink = addLinkData(pre_node_key, cur_node_key, name, attitude, dialogue_branch, dialogue_round)
            linkDataArray.append(curLink)
        else:
            # 标签节点 + 结果节点(跳转)
            answer = "{}{}".format(answer, constants.LABEL_CONTINUE)
            curData = addSlotNode(name, cur_node_key, dialogue_branch, dialogue_round * 2)
            nodeDataArray.append(curData)
            # reply_key = name + str(cur_node_key)
            reply_key = cur_node_key
            replyCollects[reply_key] = answer
            curLink = addLinkData(pre_node_key, cur_node_key, name, attitude, dialogue_branch, dialogue_round)
            linkDataArray.append(curLink)
            cur_node_key = cur_node_key - 1
            # 转人工
            dialogue_name = getDialogueName(content)
            interface_name = ""
            if dialogue_name is not None and "实时转接" == dialogue_name:
                transferName = "直接转人{}".format(random.randint(1, 100))
                transferData = addSlotNode(transferName, cur_node_key, dialogue_branch, dialogue_round * 2 + 0.5)
                nodeDataArray.append(transferData)
                # reply_key = transferName + str(cur_node_key)
                reply_key = cur_node_key
                replyCollects[reply_key] = ""
                transferLink = addLinkData(cur_node_key+1, cur_node_key, "", "", 0)
                linkDataArray.append(transferLink)
                cur_node_key = cur_node_key - 1
                interface_name = "接口调用"
            node_id = long(getDialogueIdByContext(workspace_id, version_id, content, cookie))
            nodeDataEnd = addEndNode(cur_node_key, dialogue_branch, dialogue_round * 2 + 1, "JUMP_DIALOGUE", node_id)
            nodeDataArray.append(nodeDataEnd)
            nextLink = addLinkData(cur_node_key+1, cur_node_key, "", interface_name, 0)
            linkDataArray.append(nextLink)
    flow = {
        "nodeDataArray": nodeDataArray,
        "linkDataArray": linkDataArray,
        "replyCollects": replyCollects
    }
    return flow


# 加链接数据
def addLinkData(from_key=None, to_key=None, desc="为空", title="", number=0, dialogue_round=0):
    express = ""
    compare_type = "IS_BLANK"
    value = "空"
    if "首句" in title or "接口调用" == title:
        desc = ''
        number = 0
        compare_type = "OTHERS"
        value = "获取成功"
    elif constants.ACTION_QUIET in title:
        express = '#if($!session.query == "@@quiet@@") 1 #end'
        compare_type = "EQUALS"
        value = "1"
    elif ("其他" in title and "其他平台" not in title) or "无明确回应" in title or title == "" or title == '' or title is None:
        desc = "为空"
        if "其他" in title and "男" in title:
            express = '#if("${session.queryAttitude}" == "无" && ' \
                      '$!{slot.share_userinfo.value.sexByChineseWord} == "先生") 1 #end'
            compare_type = "EQUALS"
            value = "1"
            desc = "其他-男"
        elif "其他" in title and "女" in title:
            express = '#if("${session.queryAttitude}" == "无" && ' \
                      '$!{slot.share_userinfo.value.sexByChineseWord} == "女士") 1 #end'
            compare_type = "EQUALS"
            value = "1"
            desc = "其他-女"
        else:
            number = 0
    elif "否定" in title:
        express = '#if("${session.queryAttitude}" == "否") 1 #end'
        compare_type = "EQUALS"
        value = "1"
    elif "肯定" in title:
        express = '#if("${session.queryAttitude}" == "是") 1 #end'
        compare_type = "EQUALS"
        value = "1"
    elif "不需要返回" in title:
        express = '#if($!{slot.share_guide_noneed.value} == 1) 1 #end'
        compare_type = "EQUALS"
        value = "1"
    elif "FAQ" in title:
        express = '#if("$!FaqResult.a" != "") 1 #end'
        if "高意向" in title:
            express = '#if("$!FaqResult.a" != "" && $!{slot.share_high_interest.value} == 1) 1 #end'
        if "中意向" in title:
            express = '#if("$!FaqResult.a" != "" && $!{slot.share_middle_interest.value} == 1) 1 #end'
        compare_type = "EQUALS"
        value = "1"
    else:
        title = title.replace("/", ",")
        title = title.replace("\n", ",")
        faq_title_list = title.split(",")
        faq_express = ""
        if dialogue_round == 1:
            for faq in faq_title_list:
                faq_express = faq_express + ' $!{FaqResult.standard_query} == "' + faq + '" ||'
        else:
            for faq in faq_title_list:
                faq_express = faq_express + ' $!{slot.share_' + SHARE_NAME + '_' + \
                              constants.KNOWN[dialogue_round] + '.value} == "' + faq + '" ||'
                # faq_express = faq_express + ' $!{FaqResult.standard_query} == "' + faq + '" ||'
        if faq_express != "":
            faq_express = faq_express[0:len(faq_express)-2]
        express = "#if({}) 1 #end".format(faq_express)
        compare_type = "EQUALS"
        value = "1"
    linkData = {
            "from": from_key,
            "text": desc,
            "condition": {
                "conditionValue": value,
                "compareType": compare_type,
                "conditionDesc": desc,
                "conditionExpress": express,
                "number": number
            },
            "to": to_key
        }
    return linkData


# 从文档中生成对话流程
def dealWorkspace(workspace_id, version_id, dialogue_id, cookie):
    flow = createSlotsNew(workspace_id, version_id, cookie)
    nodeDataArray = flow["nodeDataArray"]
    linkDataArray = flow["linkDataArray"]
    replyCollects = flow["replyCollects"]
    for index in range(1, len(nodeDataArray)):
        data = nodeDataArray[index]
        if str(data["text"]) == "结果":
            if str(data["type"]) == "RETURN_DIALOGUE":
                pass
            elif str(data["type"]) == "JUMP_DIALOGUE":

                # data["id"] = getJumpDialogueId(data["id"], old_workspace_id, old_cookie, workspace_id,
                #                                version_id, cookie)
                # Todo 跳转流程后面加，先写默认的
                pass
            else:
                # 添加结束
                # reply_key = "{}{}".format(data["text"], data["key"])
                reply_key = data["key"]
                reply = replyCollects[reply_key]
                newFinalAct = slot_dao.setFinalAct("BUSINESS_SYSTEM", reply, workspace_id, version_id, dialogue_id, cookie)
                data["id"] = newFinalAct["id"]
            pass
        else:
            # 添加单个槽位
            # reply_key = "{}{}".format(data["text"], data["key"])
            reply_key = data["key"]
            reply = replyCollects[reply_key]
            pattern = "$!{slot.share_company.value.round}C"
            slot = None
            # if reply.find(pattern) > 0:
            #     slot = slot_dao.createSlot(data, reply, workspace_id, version_id, dialogue_id, cookie, True)
            # else:
            slot = slot_dao.createSlot(data, reply, workspace_id, version_id, dialogue_id, cookie, False)
            data["id"] = slot["slot"]["id"]
    # 添加槽位和结束节点
    flowOldJson = {
        "class": "go.GraphLinksModel",
        "modelData": {"position": "0 0"},
        "nodeDataArray": nodeDataArray,
        "linkDataArray": linkDataArray
    }
    slot_dao.commit(json.dumps(flowOldJson), workspace_id, version_id, dialogue_id, cookie)
    # Logger.info(json.dumps(flowOldJson))
    pass


# 加结果节点
def addEndNode(k, dialogue_branch, dialogue_round, node_type="LEAF", node_id=-2):
    nodeData = {
        "text": "结果",
        "id": node_id,
        "figure": "RoundedRectangle",
        "type": node_type,
        "fill": "#6FE8E8",
        "parameter1": 100,
        "key": k,
        "loc": "{} {}".format(dialogue_branch * 125 + 200, dialogue_round * 125)
    }
    return nodeData


# 加槽位节点
def addSlotNode(name, k, dialogue_branch, dialogue_round):
    nodeData = {
        "text": name,
        "id": -2,
        "figure": "RoundedRectangle",
        "type": "SLOT",
        "fill": "#FAD165",
        "parameter1": 100,
        "key": k,
        "loc": "{} {}".format(dialogue_branch * 125 + 200, dialogue_round * 125)
    }
    return nodeData


if __name__ == '__main__':
    cookie = "JSESSIONID=node0f9fuk631raguk71ag025grno44808.node0"
    dealWorkspace(8660, 587167, 652058, cookie)
    # dealWorkspace(50468, 104126, 105755, cookie)
    # createSlotsNew()


