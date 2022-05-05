from config import constants, settings


class importFileService(object):

    # 构建话术基本信息
    def buildAnswerInfo(self, number, content, user_label, flow_label, action):
        answer = ""
        if number != '':
            number = str(number).replace(settings.RECORD_ROUND, "$!{slot.share_company.value.round}C").replace("姓", constants.SURNAME)\
                .replace("名", constants.NAME)
            content = str(content).replace("【FAQ答案】+", "")
            answer = "@#{}||{}#@".format(number, content)
        if flow_label is not None and flow_label != '':
            answer = "[{}]{}".format(flow_label, answer)
        if user_label != '':
            answer = "[{}]{}".format(user_label, answer)
        # 静音
        if constants.ACTION_QUIET in action:
            answer = "{}{}".format(answer, constants.LABEL_QUIET)
        if constants.ACTION_SEND_SMS in action:
            answer = "[{}]{}".format(constants.LABEL_SEND_SMS, answer)
        if constants.ACTION_ADD_WECHAT in action:
            answer = "[{}]{}".format(constants.LABEL_ADD_WECHAT, answer)
        if constants.ACTION_SEND_SMS_COM in action or constants.LABEL_SEND_SMS_COM in action:
            answer = "[{}]{}".format(constants.LABEL_SEND_SMS_COM, answer)
        return answer

    # 跳过上一个节点
    def jumpPreNode(self, content, name):
        if content is None or content == '':
            return ""
        content = "#if($!preSlotInfo.name != '{}')\n\t@continue@\n#else\n\t{}\n#end".format(name, content)
        return content
