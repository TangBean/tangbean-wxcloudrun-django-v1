from wxcloudrun.apps.message.models import Message


class ProjectService(object):

    def __init__(self, message: Message):
        self._message = message

    def handle(self) -> str:
        return '开发中...'
