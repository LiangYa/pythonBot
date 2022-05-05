import json
from abc import ABC

import tornado.web

from controller.recording_controller import RecordingController
from controller.recording_html_controller import RecordingHtmlController
from service import interface_service, intent_service, dialogue_service, slot_service
from util.logger import Logger


class copyWorkspaceService(tornado.web.RequestHandler):
    def get(self):
        old_workspace_id = self.get_argument("old_workspace_id")
        old_cookie = self.get_argument("old_cookie")
        workspace_id = self.get_argument("workspace_id")
        version_id = self.get_argument("version_id")
        cookie = self.get_argument("new_cookie")
        # 复制从新版本复制接口
        interface_service.copyInterfaceByWorkspaceIdNew(15467, workspace_id, cookie)
        # 复制意图接口
        intent_service.copyIntent(old_workspace_id, workspace_id, version_id, old_cookie, cookie)
        # 复制对话接口
        dialogue_service.copyDialogue(workspace_id, version_id, cookie)
        # 复制单个对话接口
        # slot_service.copyByDialogueId(old_workspace_id, 1913, old_cookie, workspace_id, version_id, 37930, cookie)
        Logger.info("开始复制对话")
        # 根据空间复制对话流程接口
        slot_service.copyAllByDialogueList(old_workspace_id, old_cookie, workspace_id, version_id, cookie)
        Logger.info("复制结束")


# 复制单个对话流程
class copy_single_dialogue_service(tornado.web.RequestHandler, ABC):
    def get(self):
        old_workspace_id = self.get_argument("old_workspace_id")
        old_dialogue_id = self.get_argument("old_dialogue_id")
        old_cookie = self.get_argument("old_cookie")
        workspace_id = self.get_argument("workspace_id")
        version_id = self.get_argument("version_id")
        dialogue_id = self.get_argument("dialogue_id")
        cookie = self.get_argument("new_cookie")

        Logger.info("开始复制对话")
        # 复制单个对话接口
        slot_service.copyByDialogueId(old_workspace_id, old_dialogue_id, old_cookie, workspace_id, version_id, dialogue_id, cookie)
        Logger.info("复制结束")
        res = {"code": 200, "msg": "复制成功"}
        self.write(str(res))


app = tornado.web.Application([
    (r'/copyWorkspace/copyWorkspaceService', copyWorkspaceService),
    (r'/copyWorkspace/copySingleDialogue', copy_single_dialogue_service),
    (r'/copyWorkspace/monitor/recording/getRecording', RecordingController),
    (r'/copyWorkspace/static/recording/match.html', RecordingHtmlController),
])

# 主函数执行
if __name__ == '__main__':
    app.listen(9001)
    print('启动服务...')
    print('服务器端口：9001')
    tornado.ioloop.IOLoop.instance().start()
