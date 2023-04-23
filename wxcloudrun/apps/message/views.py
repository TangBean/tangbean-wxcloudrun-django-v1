import logging
import time

from rest_framework.response import Response
from rest_framework.views import APIView


logger = logging.getLogger('log')


class MessageDispatcherAPIView(APIView):

    def post(self, request):
        received_data = request.data
        logger.info(received_data)
        response_data = {
            'ToUserName': received_data['FromUserName'],
            'FromUserName': received_data['ToUserName'],
            'CreateTime': int(time.time()),
            'MsgType': 'text',
            'Content': 'success'
        }
        return Response(response_data)
