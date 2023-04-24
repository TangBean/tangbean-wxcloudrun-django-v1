import logging
import time

from rest_framework.response import Response
from rest_framework.views import APIView

from wxcloudrun.apps.message.domain.chain_message.chain_message_servise import ChainMsgService
from wxcloudrun.apps.message.domain.chain_project.chain_project_service import ProjectService
from wxcloudrun.apps.message.domain.gen_report.gen_report_service import GenReportService
from wxcloudrun.apps.message.models import Message
from wxcloudrun.apps.message.utils import parse_message_biz_type
from wxcloudrun.apps.message.utils import MessageBizType

logger = logging.getLogger('log')


class MessageDispatcherAPIView(APIView):

    def post(self, request):
        try:
            received_data = request.data
            logger.info(received_data)
            received_message = Message(
                msg_id=received_data['MsgId'],
                msg_type=received_data['MsgType'],
                to_user_name=received_data['ToUserName'],
                from_user_name=received_data['FromUserName'],
                create_time=received_data['CreateTime'],
                content=received_data['Content'],
            )
            received_message_biz_type = parse_message_biz_type(received_message.content)

            response_content = '未知操作，啥都没干'

            if received_message_biz_type is MessageBizType.CHAIN_MSG:
                response_content = ChainMsgService(received_message).handle()

            elif received_message_biz_type is MessageBizType.MAKE_UP_CHAIN_MSG:
                response_content = ChainMsgService(received_message).make_up_chain_msg()

            elif received_message_biz_type is MessageBizType.NEW_CHAIN_PROJECT_MSG:
                response_content = ProjectService(received_message).handle()

            elif received_message_biz_type is MessageBizType.GEN_REPORT_MSG:
                response_content = GenReportService(received_message).handle()

            response_data = {
                'ToUserName': received_data['FromUserName'],
                'FromUserName': received_data['ToUserName'],
                'CreateTime': int(time.time()),
                'MsgType': 'text',
                'Content': response_content
            }
            return Response(response_data)
        except Exception as e:
            logger.error(e)
