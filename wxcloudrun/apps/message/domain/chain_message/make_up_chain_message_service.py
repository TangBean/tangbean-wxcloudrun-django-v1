import logging
from datetime import datetime

from wxcloudrun.apps.message.models import Message, ChainMessageDaily
from wxcloudrun.apps.message.domain.chain_message.constants import PROJECT_NAME, MSG_DATE
from wxcloudrun.common.date_util import is_date_string, parse_date_string

logger = logging.getLogger('log')


class MakeUpChainMessageService(object):

    def __init__(self, message: Message):
        self._message = message

    def handle(self) -> str:
        project_message = self.parse_project_message()
        lastest_msg = ChainMessageDaily.objects \
            .filter(from_user_name=self._message.from_user_name) \
            .order_by('-message_time') \
            .first()
        if lastest_msg is not None:
            logger.info(lastest_msg.id)
            lastest_msg._project_name = project_message[PROJECT_NAME]
            lastest_msg.msg_date = project_message[MSG_DATE]
            lastest_msg.updated_time = datetime.now()
            lastest_msg.save()
            return '更新成功'
        else:
            return '更新失败，数据不存在'

    def parse_project_message(self) -> dict:
        self._message.content = self._message.content[7:]
        project_msgs = self._message.content.strip().split('\n')

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
