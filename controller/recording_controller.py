import json
from abc import ABC

from tornado.web import RequestHandler

from service.recording_service import RecordingService


class RecordingController(RequestHandler, ABC):
    def post(self):
        return_dict = {}
        company_id = self.get_argument("company_id")
        tts_model = self.get_argument("tts_model")
        faq_name = self.get_argument("faq_name", default='FAQ', strip=True)  # faq sheet
        sheet_name = self.get_argument("sheet_name", default='全流程', strip=True)  # 话术文件 sheet
        strategy_name = self.get_argument("strategy_name", default='全局策略', strip=True)  # 全局策略 sheet
        replace_num = self.get_argument("replace_num", default='1C', strip=True)  # 全局策略 sheet
        files = self.request.files.get("file")
        if files is None:
            return_dict["code"] = 200
            return_dict["msg"] = "文件为空！"
            self.write(json.dumps(return_dict).encode("utf-8").decode("unicode_escape"))
            return
        file = files[0]
        fileData = file.get("body")
        service = RecordingService()
        file_recording_set = service.create_recording_file(faq_name, sheet_name, strategy_name, fileData, replace_num)
        data_list = service.create_recording_plat(company_id, tts_model)
        not_exist = service.match_recording(file_recording_set, data_list)
        return_dict["code"] = 200
        return_dict["msg"] = not_exist
        self.write(json.dumps(return_dict).encode("utf-8").decode("unicode_escape"))


if __name__ == '__main__':
    pass
