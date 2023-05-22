import datetime

from wxcloudrun.apps.message.domain.feishu_doc.templates.base_interpreter import BaseInterpreter
from wxcloudrun.apps.message.domain.feishu_doc.templates.daily_logs_report_content_interpreter import \
    daily_logs_report_content_interpreter
from wxcloudrun.apps.message.domain.feishu_doc.templates.daily_logs_report_header_interpreter import \
    daily_logs_report_header_interpreter
from wxcloudrun.apps.message.domain.gen_report.gen_report_dto import ReportMsg


class DailyLogsReportInterpreter(BaseInterpreter):

    def __init__(self):
        super().__init__()

    def interpret(self, report_msg: ReportMsg, chain_msg_group_by_user: dict) -> list:
        res = []
        for name, content in chain_msg_group_by_user.items():
            report_header = daily_logs_report_header_interpreter.interpret(name)
            res = res + report_header

            for i in range((report_msg.end_date - report_msg.start_date).days + 1):
                cur_date = report_msg.end_date - datetime.timedelta(days=i)
                cur_date_str = cur_date.strftime('%Y%m%d')

                cur_content = ''
                if cur_date_str in content:
                    cur_content = content[cur_date_str]

                report_content = daily_logs_report_content_interpreter.interpret(cur_date, cur_content)
                res = res + report_content

        return res
