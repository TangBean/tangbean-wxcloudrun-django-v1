from datetime import datetime


class ReportMsg(object):
    project_name: str
    start_date: datetime
    end_date: datetime
    error_msg: str
    from_user_name: str

    def __init__(self):
        self.project_name = ''
        self.start_date = datetime.now()
        self.end_date = datetime.now()
        self.error_msg = ''
        self.from_user_name = ''

    def __str__(self):
        return f'project_name: {self.project_name}, ' \
               f'start_date: {self.start_date}, ' \
               f'end_date: {self.end_date}, ' \
               f'error_msg: {self.error_msg}'
