import json
import logging
import requests

from wxcloudrun.apps.message.common.http_client import FeishuHttpClient
from wxcloudrun.apps.message.domain.chain_message.constants import FEISHU_CREATE_BLOCKS_URL
from wxcloudrun.apps.message.domain.feishu_doc.feishu_auth import FeishuAuth
from wxcloudrun.apps.message.domain.feishu_doc.feishu_documents import FeishuDocuments
from wxcloudrun.apps.message.domain.feishu_doc.templates.daily_logs_report_interpreter import DailyLogsReportInterpreter
from wxcloudrun.apps.message.domain.gen_report.gen_report_dto import ReportMsg
from wxcloudrun.common.thread_pool import FEISHU_BLOCKS_THREAD_POOL

logger = logging.getLogger('log')

MAX_CHILDREN_LEN = 50


class FeishuBlocks(object):

    def __init__(self,
                 feishu_auth: FeishuAuth,
                 report_msg: ReportMsg,
                 feishu_doc: FeishuDocuments,
                 chain_msg_group_by_user: dict):
        self._feishu_auth = feishu_auth
        self._report_msg = report_msg
        self._feishu_doc = feishu_doc
        self._chain_msg_group_by_user = chain_msg_group_by_user
        self._interpreter = DailyLogsReportInterpreter()

        FEISHU_BLOCKS_THREAD_POOL.submit(self.create_blocks)

    def create_blocks(self):
        request_children = self._interpreter.interpret(
            self._report_msg,
            self._chain_msg_group_by_user
        )

        index = len(request_children)
        logger.info(f'FeishuBlocks.create_blocks, '
                    f'document_id: {self._feishu_doc.document_id}, '
                    f'request_children.len: {index}, '
                    f'feishu API total request time: {int(index / MAX_CHILDREN_LEN + 1)}')

        while MAX_CHILDREN_LEN < index:
            start = index-MAX_CHILDREN_LEN
            end = index
            self._create_blocks(request_children[start:end])
            index = index - MAX_CHILDREN_LEN
        self._create_blocks(request_children[0:index])

        logger.info(f'FeishuBlocks.create_blocks finished, '
                    f'document_id: {self._feishu_doc.document_id}')

    def _create_blocks(self, sub_request_children: list):
        logger.info(f'FeishuBlocks._create_blocks, '
                    f'document_id: {self._feishu_doc.document_id}, '
                    f'request_children.len: {len(sub_request_children)}')

        # Define the URL
        document_id = self._feishu_doc.document_id
        url = FEISHU_CREATE_BLOCKS_URL.format(document_id=document_id, block_id=document_id)

        # Define the data to be sent
        data = json.dumps({
            "index": 0,
            "children": sub_request_children
        })
        logger.debug(f'FeishuBlocks._create_blocks request_data: {data}')

        # Define the headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._feishu_auth.tenant_access_token}'
        }

        response = FeishuHttpClient.request('FeishuBlocks._create_blocks', 'POST', url,
                                            data=data, headers=headers)
        return {
            'document_revision_id': response['data']['document_revision_id'],
            'client_token': response['data']['client_token']
        }
