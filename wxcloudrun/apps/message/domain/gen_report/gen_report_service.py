from wxcloudrun.apps.message.models import Message


class GenReportService(object):

    def __init__(self, message: Message):
        self.message = message

    def handle(self) -> str:
        return '开发中...'
