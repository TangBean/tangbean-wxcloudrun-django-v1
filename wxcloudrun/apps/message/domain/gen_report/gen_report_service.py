import json
import logging

from django.db.models import QuerySet

from wxcloudrun.apps.message.domain.chain_message.constants import FEISHU_DOCUMENT_LINK_PREFIX, \
    FEISHU_FOLDER_LINK_PREFIX
from wxcloudrun.apps.message.domain.feishu_doc.feishu_auth import FeishuAuth
from wxcloudrun.apps.message.domain.feishu_doc.feishu_documents import FeishuDocuments
from wxcloudrun.apps.message.domain.gen_report.gen_report_dto import ReportMsg
from wxcloudrun.apps.message.models import Message, ChainMessageDaily
from wxcloudrun.common.date_util import is_date_string, parse_date_string

logger = logging.getLogger('log')


class GenReportService(object):

    def __init__(self, message: Message):
        self.message = message

    def handle(self) -> str:
        report_msg = self.parse_report_msg()
        if report_msg.error_msg:
            return report_msg.error_msg
        logger.info('report_msg: %s', report_msg)

        chain_msgs = ChainMessageDaily.objects.filter(
            project_name=report_msg.project_name,
            msg_date__range=(report_msg.start_date, report_msg.end_date)
        )

        chain_msg_group_by_user = self.format_chain_msg(chain_msgs)
        logger.info('chain_msg_group_by_user: %s', json.dumps(chain_msg_group_by_user))

        feishu_auth = FeishuAuth(report_msg.project_name)

        feishu_documents = FeishuDocuments(feishu_auth, report_msg)

        return f'接龙报告生成中... (如报告内容不完整，请 1min 后刷新文档)\n' \
               f'【标题】{feishu_documents.title}\n' \
               f'【链接】{FEISHU_DOCUMENT_LINK_PREFIX}{feishu_documents.document_id}\n\n' \
               f'【文件夹】{FEISHU_FOLDER_LINK_PREFIX}{feishu_auth.folder_token}'

    def parse_report_msg(self) -> ReportMsg:
        res = ReportMsg()

        self.message.content = self.message.content[7:].strip()
        msg_arr = self.message.content.split('\n')

        # Validate message
        msg_len = len(msg_arr)
        if msg_len < 2:
            res.error_msg = '信息格式错误'
            return res

        res.project_name = msg_arr[0].strip()

        date_range_msg = msg_arr[1].strip().split('-')
        if msg_len < 2:
            res.error_msg = '日期范围格式错误'
            return res

        start_date_str = date_range_msg[0].strip()
        end_date_str = date_range_msg[1].strip()

        if not is_date_string(start_date_str):
            res.error_msg = '开始日期格式错误'
            return res
        if not is_date_string(end_date_str):
            res.error_msg = '结束日期格式错误'
            return res

        try:
            res.start_date = parse_date_string(start_date_str)
            res.end_date = parse_date_string(end_date_str)
        except ValueError:
            res.error_msg = '日期格式错误，解析报错'

        return res

    def format_chain_msg(self, chain_msg_records: QuerySet) -> dict:
        res = {}
        chain_msg_list = list(chain_msg_records)
        for chain_msg in chain_msg_list:
            cur_chain_msg_dict = json.loads(chain_msg.content)
            cur_msg_date = chain_msg.msg_date
            for key, value in cur_chain_msg_dict.items():
                res[key] = {cur_msg_date.strftime('%Y%m%d'): value}
        return res
