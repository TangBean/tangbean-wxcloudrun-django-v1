import logging

from rest_framework.response import Response
from rest_framework.views import APIView


logger = logging.getLogger('log')


class MessageDispatcherAPIView(APIView):

    def post(self, request):
        received_data = request.data
        logger.info(received_data)
        # response_data = {"message": "Data received", "data": received_data}
        return Response()
