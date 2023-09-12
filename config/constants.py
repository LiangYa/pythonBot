# FAQ-分类 - start
SORT_COMPLAINT = "投诉类FAQ"
SORT_COMMON = "普通类FAQ"
SORT_QUERY = "询问加微信相关FAQ"
SORT_HIGH = "高意向FAQ"
SORT_MIDDLE = "中意向FAQ"
SORT_LOW = "低意向FAQ"

FAQ_SORT_COMPLAINT = "【@@complaintFaq@@】"
FAQ_SORT_COMMON = "【@@commonFaq@@】"
FAQ_SORT_QUERY = "【@@queryFaq@@】"
FAQ_SORT_HIGH = "【@@highIntention@@】"
FAQ_SORT_MIDDLE = "【@@middleIntention@@】"
FAQ_SORT_LOW = "【@@lowIntention@@】"

# FAQ-分类 - end

# 动作标签 - start
ACTION_END = "挂机"
ACTION_BREAK = "打断"
ACTION_SEND_SMS = "同意发加微短信"
ACTION_ADD_WECHAT = "同意加微信小码"
ACTION_QUIET = "静音"
ACTION_SEND_SMS_COM = "发短信"
ACTION_SEND_SMS_COM_M = "发短信:"

LABEL_END = "@@end@@@@notbreak@@"  # 挂机
LABEL_BREAK_END = "@@end@@"  # 挂机 打断
LABEL_SEND_SMS = "同意发加微短信"  # 发短信
LABEL_ADD_WECHAT = "同意加微信小码"  # 加微信
LABEL_QUIET = "@no_handle_quiet@"  # 静音
LABEL_CONTINUE = "@continue@"  #
LABEL_SEND_SMS_COM = "发短信"  # 发短信 普通
# LABEL_SEND_SMS_COM = "发短信"  # 发短信 普通

# 共用标签
LABEL_COMMON = {
    "预约回访": "预约回访",
    "高意向": "高意向",
    "加黑名单": "加黑名单",
    "意向加微用户": "意向加微用户",
    "同意发优惠券": "同意发优惠券",
    "发短信:达尔文7号": "发短信:达尔文7号"
}

# 贷后标签
LABEL_LOAN = {
    "通话有效": "#robotValid#",
    "承诺还款": "#promise#",
    "有收入": "#haveIncome#",
    "无收入": "#noIncome#",
    "有多头共债": "#haveManyCall#",
    "没有多方共债": "#noManyCall#",
    "承诺减免还款": "承诺减免还款",
    "确认还款标识": "确认还款标识",
    "是本人": "#self#",
    "非本人": "#notSelf#",
    "部分还": "部分还",
    "对公还款": "对公还款",
    "提供微信号": "提供微信号",
    "有还款意愿": "有还款意愿"
}


# 共用标签
LABEL_TTS = {
    "xiai": "XA",
    "shutingB": "STB",
    "nuonan": "NN",
    "wuhaoA": "WHA",
    "xiaotongY": "XTY",
    "shutingQ": "STQ",
    "shutingS": "STS",
    "jiaoxiaotongtest": "JXTTEST",
    "shutingA": "STA",
    "shutingN": "STN",
    "shutingR": "STR",
    "xiaotongW": "XTW",
    "shitong": "STO",
    "shutingK": "STK",
    "siyang": "SY",
    "jiaoxiaotong": "JXT",
    "xiaotongEE": "XTEE",
    "xiaotongQ": "XTQ",
    "ningbo": "NB",
    "yitingA": "YTA",
    "xiaotongU": "XTU",
    "qiqi": "QQ",
    "xiaotongF": "XTF",
    "xiaotongN": "XTN",
    "xiaoyu": "XY",
    "shutingG": "STG",
    "xiaotongC": "XTC",
    "xiaotongZ": "XTZ",
    "xiaotongCC": "XTCC",
    "shutingM": "STM",
    "xiaotongS": "XTS",
    "shutingJ": "STJ",
    "xiaotongL": "XTL",
    "shutingV": "STV",
    "xiaotongAA": "XTAA",
    "xttest": "XTTEST",
    "xiaotongE": "XTE",
    "xiaotongM": "XTM",
    "shuting": "ST",
    "xiaotongJ": "XTJ",
    "xiaotongP": "XTP",
    "houyu": "HY",
    "xiaotongG": "XTG",
    "xiaotongT": "XTT",
    "xiaotongB": "XTB",
    "xiaoqinA": "XQA",
    "test": "TEST",
    "tongyong": "TY",
    "shutingU": "STU",
    "xiaotongDD": "XTDD",
    "xiaotong": "XT",
    "shutingE": "STE",
    "shutingI": "STI",
    "shutingT": "STT",
    "shitongA": "STOA",
    "shutingP": "STP",
    "ziyun": "ZY",
    "shutingH": "STH",
    "xiaotongI": "XTI",
    "shutingX": "STX",
    "xintong": "ZXT",
    "wuhao": "WH",
    "xiaotongD": "XTD",
    "xiaotongK": "XTK",
    "yitingB": "YTB",
    "shutingL": "STL",
    "xiaotongH": "XTH",
    "shutingC": "STC",
    "xiaoqin": "XQ",
    "xiaotongR": "XTR",
    "shutingY": "STY",
    "liushitongtest": "LSTTEST",
    "xiaotongA": "XTA",
    "shutingF": "STF",
    "yiting": "YT",
    "xiaotongBB": "XTBB",
    "liushitong": "LST",
    "shutingD": "STD",
    "xiaotongV": "XTV",
    "zhaoshijie": "SJ",
    "shutingW": "STW"
}

# 动作标签 - end

# 分类标签
SORTS_LOAN = {
    "低意向FAQ": "【@@lowIntention@@】"
}

SURNAME = "$!{slot.share_userinfo.value.familyName}"
NAME = "$!{slot.share_userinfo.value.sexByChineseWord}"

KNOWN = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven',
         'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']

SHARE_NAME = {
    "不需要": "share_noneed",
    "什么平台": "share_platform",
    "客户会考虑": "share_consider"
}

BRANCH_NAME = ["FAQ轮询1次", "首句-无态度轮询1次", "首句-无态度轮询2次"]

REPLACE_NODE_START = "\n#if(${session.query} == \"@@quiet@@\") \n#if(${quietTime} == 1) @#T4||喂，能听到吗？#@ \n#elseif(${quietTime} == 2) @#T5||喂，听得到吗？#@ \n#end \n#end \n#if(${session.query} == \"@@quiet@@\" && ${quietTime} == 3) @#T6||电话已经接通，我确认你是可以听得到。你在我们这的欠款已经逾期，请你尽快处理，避免持续逾期对你的生活和工作产生影响。电话都有录音，我们已经将相关情况通知到你，再见。#@@@end@@@@notbreak@@ \n#elseif( ${quietTime} + ${visitTime} == 4 || ${globalVisitTime} == 6) @#T7||你的欠款已经逾期很久了，请你尽快处理，避免持续逾期对你的生活和信用产生影响。电话都有录音，我们已经将相关情况通知到你，再见。#@@@end@@@@notbreak@@ \n#elseif(${quietTime} != 3) \n#if(${globalVisitTime} == 1) \n"
REPLACE_NODE_END = "\n#else \n@continue@ \n#end \n#end"

REPLACE_NODE_FAQ = "\n#elseif(${globalVisitTime} == 2 || ${session.query} == \"@@quiet@@\")\n"

# 流程版本
FLOW_NAME = 1  # 流程环节
FLOW_LABEL_NODE = 3  # 流程节点标签
FLOW_ORDER = 4  # 流转顺序
FLOW_ATTITUDE = 5  # 流转条件
FLOW_RECORD_NUMBER = 6  # 录音编号
FLOW_WORDS = 7  # 场景话术
FLOW_LABEL_USER = 8  # 用户标签
FLOW_LABEL_ACTION = 10  # 动作标签


if __name__ == '__main__':
    # action = "承诺还款\n承诺减免还款\n通话有效"
    # action_labels = action.split("\n")
    # labels = ""
    # for label in action_labels:
    #     if label in LABEL_LOAN:
    #         labels = "{}[{}]".format(labels, LABEL_LOAN.get(label))
    # print(labels)
    pass
