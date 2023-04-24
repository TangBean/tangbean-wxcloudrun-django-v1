import re
from datetime import datetime


def is_date_string(date_string):
    """
    检查字符串是否符合类似"4.25", "5.23", "12.11", "2023.4.12"的日期格式.
    函数返回一个布尔值，表示字符串是否符合该格式
    """
    pattern = r'^(?:(\d{4}\.)?)\d{1,2}\.\d{1,2}$'
    return bool(re.match(pattern, date_string))


def parse_date_string(date_string):
    current_year = datetime.now().year

    # Check if the date string contains a year.
    if len(date_string.split('.')) == 3:
        year, month, day = map(int, date_string.split('.'))
    else:
        year = current_year
        month, day = map(int, date_string.split('.'))

    return datetime(year, month, day)
