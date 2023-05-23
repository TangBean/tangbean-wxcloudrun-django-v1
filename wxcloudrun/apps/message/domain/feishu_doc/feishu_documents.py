import json
import logging

from wxcloudrun.apps.message.common.http_client import FeishuHttpClient
from wxcloudrun.apps.message.domain.chain_message.constants import FEISHU_CREATE_DOCUMENT_URL, \
    FEISHU_UPDATE_PERMISSION_URL
from wxcloudrun.apps.message.domain.feishu_doc.feishu_auth import FeishuAuth
from wxcloudrun.apps.message.domain.gen_report.gen_report_dto import ReportMsg

logger = logging.getLogger('log')


class FeishuDocuments(object):

    def __init__(self, feishu_auth: FeishuAuth, report_msg: ReportMsg):
        self._feishu_auth = feishu_auth
        self._report_msg = report_msg

        self._headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._feishu_auth.tenant_access_token}'
        }

        self._title = self._build_document_title()
        self._document_id = self._create_document()
        self._update_permissions()

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

        response = FeishuHttpClient.request('FeishuDocuments._create_document', 'POST', url,
                                            data=data, headers=self._headers)
        return response['data']['document']['document_id']

    def _update_permissions(self):
        # Define the URL
        url = FEISHU_UPDATE_PERMISSION_URL.format(document_id=self._document_id)

        # Define the data to be sent
        data = json.dumps({
          "external_access_entity": "open",
          "security_entity": "anyone_can_view",
          "comment_entity": "anyone_can_view",
          "link_share_entity": "anyone_editable",
          "copy_entity": "anyone_can_view"
        })

        # Define the params to be sent
        params = {'type': 'docx'}

        response = FeishuHttpClient.request('FeishuDocuments._update_permissions', 'PATCH', url,
                                            params=params, data=data, headers=self._headers)
        return response['msg']
