import json
import random
import time

import xlrd
from numpy.compat import long

import util
from config import constants
from controller.file_input_test import read_file3
from service.dialogue_service import getDialogueIdByContext, getDialogueName, getDialogueList
from service.import_file_service import importFileService
from util.comUtil import CommonUtil
from util.logger import Logger
from util.merge_cell_util import get_cell_type
from dao import slot_dao


SHARE_NAME = ""
def create_name():
    global SHARE_NAME
    # random_number = random.randint(1, 100)
    # SHARE_NAME = "{}".format(random_number)
    # 获取当前时间的时间戳（秒数）
    timestamp = int(time.time())
    SHARE_NAME = "{}".format(timestamp)
    # print(SHARE_NAME)


cur_dialogue_list = None
def get_dialogue_list(workspace_id, version_id, cookie):
    global cur_dialogue_list
    cur_dialogue_list = getDialogueList(workspace_id, version_id, cookie)


def getDialogueId(dialogue_name):
    if cur_dialogue_list is None:
        return None
    dialogue_id = -2
    for dialogue in cur_dialogue_list:
        if dialogue_name == dialogue["name"]:
            dialogue_id = "{}".format(dialogue["id"])
            Logger.info("dialogue_id:{}, dialogue_name:{}".format(dialogue["id"], dialogue["name"]))
            break
    return dialogue_id

# Excel导入流程
# 京东-新平台创建对话流程
def createSlotsNew(workspace_id, version_id, path, sheetName, index_start, index_end, cookie):
    readBook = xlrd.open_workbook(r'../excel/{}'.format(path))
    # sheetFaq = readBook.sheet_by_index(0)
    sheetFaq = readBook.sheet_by_name(sheetName)
    nrows = sheetFaq.nrows  # 行
    ncols = sheetFaq.ncols  # 列
    nodeDataArray = [
        {
            "text": "开始",
            "id": -1,
            "figure": "RoundedRectangle",
            "type": "DIALOGUE",
            "parameter1": 100,
            "loc": "310 0",
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
            "loc": "310 150"
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
    # replyCollects = {
    #     "记录开始-2": ""
    # }
    replyCollects = {
        "-2": ""
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
    for i in range(index_start, index_end):
        # label2 = sheetFaq.cell(i, 4).value
        reverseOrder = sheetFaq.cell(i, constants.FLOW_ORDER).value
        if reverseOrder == 1.0:
            reverseOrder = 1
        attitude = sheetFaq.cell(i, constants.FLOW_ATTITUDE).value
        number = sheetFaq.cell(i, constants.FLOW_RECORD_NUMBER).value
        label = sheetFaq.cell(i, constants.FLOW_LABEL_USER).value
        content = sheetFaq.cell(i, constants.FLOW_WORDS).value
        action = sheetFaq.cell(i, constants.FLOW_LABEL_ACTION).value
        merged = sheetFaq.merged_cells
        label2 = get_cell_type(i, constants.FLOW_LABEL_NODE, merged, sheetFaq)
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
        if (number != '' and constants.ACTION_END not in action) or \
                (number != '' and constants.ACTION_END in action and constants.ACTION_BREAK in action):
            # 1.槽位节点
            # 1.1创建下一个槽位
            if next_node_key is None:
                next_node_name = "分流_{}".format(random.randint(1, 100))
                next_node_key = cur_node_key
                nextData = addSlotNode(next_node_name, next_node_key, dialogue_branch, dialogue_round * 2 + 1, dialogue_round)
                nodeDataArray.append(nextData)
                # reply_key = next_node_name + str(next_node_key)
                reply_key = str(next_node_key)
                replyCollects[reply_key] = ""
                cur_node_key = cur_node_key - 1
            # 1.2创建当前槽位
            curData = addSlotNode(name, cur_node_key, dialogue_branch, dialogue_round * 2)
            nodeDataArray.append(curData)
            # reply_key = name + str(cur_node_key)
            reply_key = str(cur_node_key)
            # 1.2.1 添加判断跳过上一个节点
            answer = impFileService.jumpPreNode(answer, pre_node_name)
            if number != '' and constants.ACTION_END in action and constants.ACTION_BREAK in action:
                answer = "{}{}".format(answer.replace("#end", ""), constants.LABEL_BREAK_END)
                answer = "{}{}".format(answer, "\n#end")
            replyCollects[reply_key] = answer
            # 1.3建立关系-上一个节点和当前关系，当前节点和下一个节点关系
            curLink = addLinkData(pre_node_key, cur_node_key, name, attitude, dialogue_branch,
                                  dialogue_round=dialogue_round)
            nextLink = addLinkData(cur_node_key, next_node_key, "", "", 0, 0)
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
            reply_key = str(cur_node_key)
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
            reply_key = str(cur_node_key)
            replyCollects[reply_key] = answer
            curLink = addLinkData(pre_node_key, cur_node_key, name, attitude, dialogue_branch, dialogue_round)
            linkDataArray.append(curLink)
            cur_node_key = cur_node_key - 1
            # 转人工
            dialogue_name = getDialogueName(content)
            interface_name = ""
            # if dialogue_name is not None and "实时转接" == dialogue_name:
            #     transferName = "直接转人{}".format(random.randint(1, 100))
            #     transferData = addSlotNode(transferName, cur_node_key, dialogue_branch, dialogue_round * 2 + 0.5)
            #     nodeDataArray.append(transferData)
            #     reply_key = transferName + str(cur_node_key)
            #     replyCollects[reply_key] = ""
            #     transferLink = addLinkData(cur_node_key+1, cur_node_key, "", "", 0)
            #     linkDataArray.append(transferLink)
            #     cur_node_key = cur_node_key - 1
            #     interface_name = "接口调用"
            node_id = long(getDialogueIdByContext(workspace_id, version_id, content, cookie))
            nodeDataEnd = addEndNode(cur_node_key, dialogue_branch, dialogue_round * 2 + 1, "JUMP_DIALOGUE", node_id)
            nodeDataArray.append(nodeDataEnd)
            nextLink = addLinkData(cur_node_key+1, cur_node_key, "", interface_name, 0)
            linkDataArray.append(nextLink)

        if attitude == "静音":
            dealQuiet(pre_node_key, linkDataArray, replyCollects)
    flow = {
        "nodeDataArray": nodeDataArray,
        "linkDataArray": linkDataArray,
        "replyCollects": replyCollects
    }
    return flow


def dealQuiet(pre_node_key, linkDataArray, replyCollects):
    if pre_node_key is None or linkDataArray is None or replyCollects is None:
        return
    fromList = []
    for linkData in linkDataArray:
        if "to" in linkData and pre_node_key == linkData['to']:
            fromList.append(linkData['from'])
    if len(fromList) > 0:
        for one in fromList:
            reply = replyCollects.get(str(one))
            if reply:
                reply = reply.replace("\n#end", "@no_handle_quiet@\n#end")
                replyCollects[str(one)] = reply


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
    elif "不需要-使用其他平台" not in title and ("其他" in title or "无明确回应" in title):
        express = "1"
        value = "1"
        compare_type = "EQUALS"
        # number = 0
        desc = ""
    elif "不需要-使用其他平台" not in title and ("其他" in title or "无明确回应" in title
                                        or "" == title or '' == title or title is None):
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
        express = '#if($!{slot.share_guide_noneed_return.value} == 1 && $preDialogue.name == "返回原流程") 1 #end'
        compare_type = "EQUALS"
        value = "1"
    elif "FAQ" in title:
        express = '#if("$!FaqResult.a" != "") 1 #end'
        # express = '#if("$!FaqResult.a" != "" || ("$!preDialogue.name" != "" && $!preDialogue.name != "确认是否打开APP")) 1 #end'
        if "高意向" in title:
            express = '#if("$!FaqResult.a" != "" && $!{slot.share_high_interest.value} == 1) 1 #end'
        if "中意向" in title:
            express = '#if("$!FaqResult.a" != "" && $!{slot.share_middle_interest.value} == 1) 1 #end'
        compare_type = "EQUALS"
        value = "1"
    else:
        # title = title.replace("/", ",")
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
def dealWorkspace(workspace_id, version_id, dialogue_id,
                  path, sheetName, index_start, index_end, cookie):
    flow = createSlotsNew(workspace_id, version_id, path, sheetName, index_start, index_end, cookie)
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
                reply_key = "{}".format(data["key"])
                reply = replyCollects[reply_key]
                newFinalAct = slot_dao.setFinalAct("BUSINESS_SYSTEM", reply, workspace_id, version_id, dialogue_id, cookie)
                data["id"] = newFinalAct["id"]
            pass
        else:
            # 添加单个槽位
            # reply_key = "{}{}".format(data["text"], data["key"])
            reply_key = "{}".format(data["key"])
            reply = replyCollects[reply_key]
            transfer_one = "@@transfer@@{transfer_success-MTC34||好的，您不要挂机哦，马上为您服务@@notbreak@@}"
            transfer_two = "@@transfer@@{transfer_success-$!{slot.share_faqrs.value}MTC35||您不要挂机哈，专业的客户经理马上为您服务@@notbreak@@}"
            if "主流程【有坐席接起】】" in reply:
                reply = reply.replace("【主流程【有坐席接起】】", "")
                reply = reply.replace("#end", "{}\n#end".format(transfer_one))
            elif "【命中FAQ【有坐席接起】】" in reply:
                reply = reply.replace("【命中FAQ【有坐席接起】】", "")
                reply = reply.replace("#end", "{}\n#end".format(transfer_two))
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
        "loc": "{} {}".format(dialogue_branch * 110 + 200, dialogue_round * 150)
    }
    return nodeData


# 加槽位节点
def addSlotNode(name, k, dialogue_branch, dialogue_round, known_key=0):
    nodeData = {
        "text": name,
        "id": -2,
        "figure": "RoundedRectangle",
        "type": "SLOT",
        "fill": "#FAD165",
        "parameter1": 100,
        "key": k,
        "loc": "{} {}".format(dialogue_branch * 110 + 200, dialogue_round * 150)
    }
    if known_key != 0:
        nodeData["identity"] = "share_" + SHARE_NAME + "_" + constants.KNOWN[known_key+1]
    return nodeData


if __name__ == '__main__':
    cookie = "JSESSIONID=node0qrgcwwjw6o6915wop3q5w4n5c3276461.node0"
    workspace_id = 1157087
    version_id = 1145024
    path = "度小满人机-聚合支付收款码-0901.xlsx"
    sheetName = "度小满人机-聚合支付收款码-0901"
    dialogueList = read_file3(path, sheetName)
    get_dialogue_list(workspace_id, version_id, cookie)
    for dialogue in dialogueList:
        create_name()
        dialogue_name = dialogue[0]
        index_start = dialogue[1]-1
        index_end = dialogue[2]
        dialogue_id = getDialogueId(dialogue_name)
        # print("流程：{},{}".format(dialogue_name, dialogue_id))
        print("{}".format(dialogue_name))
        # if dialogue_name == "核身环节":
        # if dialogue_name not in ["核身环节"]:
        if dialogue_name in ["度小满公众号操作流程","度小满公众号操作流程-登录账号","度小满公众号操作流程-寻找立即入驻图标"]:
            dealWorkspace(workspace_id, version_id, dialogue_id,
                          path, sheetName, index_start, index_end, cookie)
            print(dialogue_name)

