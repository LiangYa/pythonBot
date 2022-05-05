from abc import ABC

from tornado.web import RequestHandler

from config.settings import BASE_DIR


class RecordingHtmlController(RequestHandler, ABC):
    def get(self):
        html_path = "{}/static/recording.html".format(BASE_DIR)
        self.render(html_path)


if __name__ == '__main__':
    print(BASE_DIR)
    pass
