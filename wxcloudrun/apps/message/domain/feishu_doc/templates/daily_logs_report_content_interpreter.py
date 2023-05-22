from datetime import datetime

from wxcloudrun.apps.message.domain.chain_message.constants import DAILY_LOGS_DATE_PLACEHOLDER, \
    DAILY_LOGS_CONTENT_PLACEHOLDER
from wxcloudrun.apps.message.domain.feishu_doc.templates.base_interpreter import BaseInterpreter


class DailyLogsReportContentInterpreter(BaseInterpreter):

    def __init__(self):
        super().__init__()

    def interpret(self, daily_logs_date: datetime, daily_logs_content: str) -> list:
        data = self._load_request_template(
            file_name='daily_logs_report_content_template.json',
            invoke_file=__file__,
            replace_map={
                DAILY_LOGS_DATE_PLACEHOLDER: daily_logs_date.strftime("%m.%d (%a)"),
                DAILY_LOGS_CONTENT_PLACEHOLDER: daily_logs_content,
            }
        )
        if not daily_logs_content:
            data.pop()
        return data


daily_logs_report_content_interpreter = DailyLogsReportContentInterpreter()
