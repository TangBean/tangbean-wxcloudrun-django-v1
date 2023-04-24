import logging
from datetime import datetime

from wxcloudrun.apps.message.models import Message, ChainProject, ChainMessageDaily
from wxcloudrun.apps.message.utils import MessageBizType
from wxcloudrun.common.date_util import is_date_string, parse_date_string
from wxcloudrun.common.exceptions import InvalidInputException

logger = logging.getLogger('log')

PROJECT_NAME = 'project_name'
MSG_DATE = 'msg_date'


class ChainMsgService(object):

    def __init__(self, message: Message):
        self.message = message

    def handle(self) -> str:
        project_message = self.parse_project_message()
        is_valid_project = self.project_name_exists(project_message[PROJECT_NAME])
        if not is_valid_project:
            project_message[PROJECT_NAME] = None
            project_message[MSG_DATE] = None
        new_msg = ChainMessageDaily(
            content=self.message.content,
            to_user_name=self.message.to_user_name,
            from_user_name=self.message.from_user_name,
            msg_id=self.message.msg_id,
            message_time=self.message.create_time,
            project_name=project_message[PROJECT_NAME],
            msg_date=project_message[MSG_DATE],
        )
        new_msg.save()
        if is_valid_project:
            return f'接龙消息写入成功！\n' \
                   f'项目名称: {project_message[PROJECT_NAME]}\n' \
                   f'消息日期:{project_message[MSG_DATE]}'
        else:
            return f'接龙消息写入成功，但项目信息不完整，请按如下格式回复 项目名称 和 消息日期：\n' \
                   f'{MessageBizType.MAKE_UP_CHAIN_MSG}\n' \
                   f'【项目名称】\n' \
                   f'【消息日期，格式：%m.%d / %Y.%m.%d】'

    def make_up_chain_msg(self) -> str:
        return '开发中...'

    def parse_project_message(self) -> dict:
        """
        Parse message.

        :raises InvalidInputException: If self.message.content not contain '1. '.
        """
        self.message.content = self.message.content[3:]
        pos = self.message.content.find('1. ')
        if pos == -1:
            raise InvalidInputException

        project_msgs = self.message.content[:pos].strip().split('\n')
        self.message.content = self.message.content[pos:]

        msg_len = len(project_msgs)
        if msg_len < 1:
            return {}
        project_name = project_msgs[0].strip()

        msg_date = None
        for msg in project_msgs[1:]:
            msg = msg.strip()
            if is_date_string(msg):
                try:
                    msg_date = parse_date_string(msg)
                except ValueError:
                    pass
        if not msg_date:
            msg_date = datetime.now()

        return {
            PROJECT_NAME: project_name,
            MSG_DATE: msg_date,
        }

    def project_name_exists(self, project_name) -> bool:
        return ChainProject.objects.filter(project_name=project_name).exists()
