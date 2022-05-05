from config import constants
from dao.recording_dao import getRecordManageList
from util.logger import reload_log
from util.operate_excel import OperateExcel


class RecordingService:
    def __init__(self):
        self.log = reload_log()
        self.excel = OperateExcel()
        pass

    # 匹配录音编号是否存在平台中的录音编号
    def match_recording(self, file_recording_set, data_set):
        not_exist = []
        if len(file_recording_set) == 0:
            self.log.error("文件录音编号为空")
        if len(data_set) == 0:
            self.log.error("获取平台录音编号为空")
        for recording in file_recording_set:
            if recording not in data_set:
                not_exist.append(recording)
        return not_exist

    # 构建平台录音编号
    def create_recording_plat(self, company_id, tts_model):
        dataList = getRecordManageList(company_id, tts_model)
        dataSet = set()
        if dataList is None or dataList[0]["list"] == []:
            return dataSet
        for model in dataList[0]["list"]:
            dataSet.add(model['fileName'])
        self.log.info("创建 平台录音列表")
        return dataSet

    # 构建文件录音编号
    def create_recording_file(self, faq_name, sheet_name, strategy_name, file_data, replace_num):
        file_recording_set = set()
        # self.excel.get_recording_list(file_data, sheet_name, 2, 7, replace_num, file_recording_set)
        # self.excel.get_recording_list(file_data, faq_name, 1, 1, replace_num, file_recording_set)
        # self.excel.get_recording_list(file_data, strategy_name, 1, 4, replace_num, file_recording_set)
        self.excel.get_recording_list_pandas(file_data, sheet_name, replace_num, file_recording_set)
        self.excel.get_recording_list_pandas(file_data, faq_name, replace_num, file_recording_set)
        self.excel.get_recording_list_pandas(file_data, strategy_name, replace_num, file_recording_set)
        self.log.info("完成 创建文件录音列表")
        if constants.OPENING_SURNAME in file_recording_set:
            self.create_opening(file_recording_set)
            file_recording_set.remove(constants.OPENING_SURNAME)
        return file_recording_set

    def create_opening(self, file_recording_set):
        self.log.info('创建 开场-百家姓')
        for surname in constants.HUNDRED_SURNAMES:
            file_recording_set.add('开场-{}女士'.format(surname))
            file_recording_set.add('开场-{}先生'.format(surname))


if __name__ == '__main__':
    service = RecordingService()
    # eeee = service.create_recording_set(2137, "shuting")
    service.create_opening(None)
    pass
