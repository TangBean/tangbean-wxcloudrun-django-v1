import json
import logging
from datetime import datetime

from django.db.models import QuerySet

from wxcloudrun.apps.message.models import Message, ChainMessageDaily
from wxcloudrun.common.date_util import is_date_string, parse_date_string

logger = logging.getLogger('log')


class GenReportService(object):

    def __init__(self, message: Message):
        self.message = message

    def handle(self) -> str:
        report_msg = self.parse_report_msg()
        if report_msg['error_msg']:
            return report_msg['error_msg']
        logger.info('report_msg', report_msg)

        chain_msg_records = ChainMessageDaily.objects.filter(
            project_name=report_msg['project_name'],
            msg_date__range=(report_msg['start_date'], report_msg['end_date'])
        )

        chain_msg_group_by_user = self.format_chain_msg(chain_msg_records)
        logger.info('chain_msg_group_by_user', chain_msg_group_by_user)

        return '开发中...'

    def parse_report_msg(self) -> dict:
        self.message.content = self.message.content[7:].strip()
        msg_arr = self.message.content.split('\n')

        # Validate message
        msg_len = len(msg_arr)
        if msg_len < 2:
            return {
                'error_msg': '信息格式错误'
            }

        project_name = msg_arr[0].strip()
        date_range_msg = msg_arr[1].strip().split('-')
        if msg_len < 2:
            return {
                'error_msg': '日期范围格式错误'
            }

        start_date_str = date_range_msg[0].strip()
        end_date_str = date_range_msg[1].strip()

        if not is_date_string(start_date_str):
            return {
                'error_msg': '开始日期格式错误'
            }
        if not is_date_string(end_date_str):
            return {
                'error_msg': '结束日期格式错误'
            }

        try:
            start_date = parse_date_string(start_date_str)
            end_date = parse_date_string(end_date_str)
            return {
                'project_name': project_name,
                'start_date': start_date,
                'end_date': end_date
            }
        except ValueError:
            pass
        return {
            'error_msg': '日期格式错误，解析报错'
        }

    def format_chain_msg(self, chain_msg_records: QuerySet) -> dict:
        res = {}
        chain_msg_list = list(chain_msg_records)
        for chain_msg in chain_msg_list:
            cur_chain_msg_dict = json.loads(chain_msg.content)
            cur_msg_date = chain_msg.msg_date
            for key, value in cur_chain_msg_dict.items():
                res[key][cur_msg_date] = value
        return res
