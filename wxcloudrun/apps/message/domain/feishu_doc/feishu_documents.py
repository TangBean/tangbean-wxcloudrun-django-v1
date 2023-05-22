import json
import logging

import requests

from wxcloudrun.apps.message.domain.chain_message.constants import FEISHU_CREATE_DOCUMENT_URL
from wxcloudrun.apps.message.domain.feishu_doc.feishu_auth import FeishuAuth
from wxcloudrun.apps.message.domain.gen_report.gen_report_dto import ReportMsg
from wxcloudrun.common.exceptions import HttpRequestException, ExternalServerException

logger = logging.getLogger('log')


class FeishuDocuments(object):

    def __init__(self, feishu_auth: FeishuAuth, report_msg: ReportMsg):
        self._feishu_auth = feishu_auth
        self._report_msg = report_msg
        self._title = self._build_document_title()
        self._document_id = self._create_document()

    @property
    def title(self):
        return self._title

    @property
    def document_id(self):
        return self._document_id

    def _build_document_title(self):
        return f'{self._report_msg.start_date.strftime("%Y%m%d")} - ' \
               f'{self._report_msg.end_date.strftime("%Y%m%d")}'

    def _create_document(self):
        # Define the URL
        url = FEISHU_CREATE_DOCUMENT_URL

        # Define the data to be sent
        data = json.dumps({
            "folder_token": self._feishu_auth.folder_token,
            "title": self._title
        })
        logger.debug(f'FeishuDocuments._create_document request_data: {data}')

        # Define the headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._feishu_auth.tenant_access_token}'
        }

        # Send the POST request
        response = requests.post(url, data=data, headers=headers)

        # Check the status code
        if response.status_code == 200:
            response_json = json.loads(response.content)

            if response_json['code'] != 0:
                error_msg = f'FeishuDocuments._create_document ExternalServerException, ' \
                            f'code: {response_json["code"]}, ' \
                            f'msg: {response_json["msg"]}'
                logger.error(error_msg)
                raise ExternalServerException(error_msg)

            return response_json['data']['document']['document_id']

        else:
            error_msg = f'FeishuDocuments._create_document HttpRequestException, ' \
                        f'status_code: {response.status_code}, ' \
                        f'content: {response.content}'
            logger.error(error_msg)
            raise HttpRequestException(error_msg)
