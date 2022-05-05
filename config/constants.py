# FAQ-分类 - start
SORT_COMPLAINT = "投诉类FAQ"
SORT_COMMON = "普通类FAQ"
SORT_QUERY = "询问加微信相关FAQ"
SORT_HIGH = "高意向FAQ"
SORT_MIDDLE = "中意向FAQ"

FAQ_SORT_COMPLAINT = "【@@complaintFaq@@】"
FAQ_SORT_COMMON = "【@@commonFaq@@】"
FAQ_SORT_QUERY = "【@@queryFaq@@】"
FAQ_SORT_HIGH = "【@@highIntention@@】"
FAQ_SORT_MIDDLE = "【@@middleIntention@@】"

# FAQ-分类 - end

# 动作标签 - start
ACTION_END = "挂机"
ACTION_BREAK = "打断"
ACTION_SEND_SMS = "同意发加微短信"
ACTION_ADD_WECHAT = "同意加微信小码"
ACTION_QUIET = "静音"
ACTION_SEND_SMS_COM = "发短信"

LABEL_END = "@@end@@@@notbreak@@"  # 挂机
LABEL_BREAK_END = "@@end@@"  # 挂机 打断
LABEL_SEND_SMS = "同意发加微短信"  # 发短信
LABEL_ADD_WECHAT = "同意加微信小码"  # 加微信
LABEL_QUIET = "@no_handle_quiet@"  # 静音
LABEL_CONTINUE = "@continue@"  #
LABEL_SEND_SMS_COM = "#message#"  # 发短信 普通
# 动作标签 - end


SURNAME = "$!{slot.share_userinfo.value.familyName}"
NAME = "$!{slot.share_userinfo.value.sexByChineseWord}"

KNOWN = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven',
         'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']

SHARE_NAME = {
    "不需要": "share_noneed",
    "什么平台": "share_platform",
    "客户会考虑": "share_consider"
}

