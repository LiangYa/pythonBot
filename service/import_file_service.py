from config import constants, settings


class importFileService(object):

    # 构建话术基本信息
    def buildAnswerInfo(self, number, content, user_label, flow_label, action):
        answer = ""
        if number != '':
            number = str(number).replace(settings.RECORD_ROUND, "$!{slot.share_company.value.round}C").replace("姓", constants.SURNAME)\
                .replace("名", constants.NAME)
            content = str(content).replace("【FAQ答案】+", "").replace("【faq答案】+", "")
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
        # 贷后标签
        answer = "{}{}".format(self.add_loan_label(action), answer)
        # 电销标签
        answer = "{}{}".format(self.add_common_label(action), answer)
        return answer

    # 添加贷后标签
    def add_loan_label(self, action):
        if action is None or action == "":
            return ""
        action_labels = action.split("\n")
        labels = ""
        for label in action_labels:
            if label in constants.LABEL_LOAN:
                labels = "{}[{}]".format(labels, constants.LABEL_LOAN.get(label))
        return labels

    # 添加电销标签
    def add_common_label(self, action):
        if action is None or action == "":
            return ""
        action_labels = action.split("\n")
        labels = ""
        for label in action_labels:
            if label in constants.LABEL_COMMON:
                labels = "{}[{}]".format(labels, constants.LABEL_COMMON.get(label))
        return labels

    # 跳过上一个节点
    def jumpPreNode(self, content, name):
        if content is None or content == '':
            return ""
        content = "#if($!preSlotInfo.name != '{}')\n\t@continue@\n#else\n\t{}\n#end".format(name, content)
        return content

    # 拼接
    def jumpPreNodeTwo(self, content, name):
        if content is None or content == '':
            return ""
        for temp_name in constants.BRANCH_NAME:
            if temp_name in name:
                return content
        content = "{}{}{}".format(constants.REPLACE_NODE_START, content, constants.REPLACE_NODE_END)
        return content

    # 拼接
    def jumpPreNodeTwoFAQ(self, content, replyCollects, pre_node_key):
        if content is None or content == '' or replyCollects is None:
            return ""
        contentTemp = replyCollects[pre_node_key]
        answer = "{}{}{}{}".format(str(contentTemp).replace(constants.REPLACE_NODE_END, ""),
                                   constants.REPLACE_NODE_FAQ, content, constants.REPLACE_NODE_END)
        replyCollects[pre_node_key] = answer
        return answer