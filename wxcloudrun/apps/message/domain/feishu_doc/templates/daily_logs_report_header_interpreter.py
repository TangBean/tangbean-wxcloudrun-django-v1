from wxcloudrun.apps.message.domain.chain_message.constants import USER_NAME_PLACEHOLDER
from wxcloudrun.apps.message.domain.feishu_doc.templates.base_interpreter import BaseInterpreter


class DailyLogsReportHeaderInterpreter(BaseInterpreter):

    def __init__(self):
        super().__init__()

    def interpret(self, user_name: str) -> list:
        data = self._load_request_template(
            file_name='daily_logs_report_header_template.json',
            invoke_file=__file__,
            replace_map={
                USER_NAME_PLACEHOLDER: user_name
            }
        )
        return data


daily_logs_report_header_interpreter = DailyLogsReportHeaderInterpreter()
