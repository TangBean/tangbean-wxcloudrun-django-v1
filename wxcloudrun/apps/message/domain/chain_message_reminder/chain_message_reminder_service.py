import logging
from datetime import time
from typing import Sequence

from wxcloudrun.apps.message.domain.chain_message_reminder.chain_message_reminder_dto import GetUpData
from wxcloudrun.apps.message.models import Message
from wxcloudrun.apps.message.utils import parse_message_content_without_format, parse_first_integer

logger = logging.getLogger('log')

VALID_LOG_MIN_LEN = 5
GET_UP_LATE_TIME = time(8)

USER_NAME_PLACEHOLDER = '[[USER_NAME_PLACEHOLDER]]'

UNLOG_REMINDER_COPYWRITE_TEMPLATE = "Hi，[[USER_NAME_PLACEHOLDER]]，记得更新今天的早起日志哦 (*^▽^*)"
GET_UP_LATE_REMINDER_COPYWRITE_TEMPLATE = "Hi，[[USER_NAME_PLACEHOLDER]]，今天的起床时间晚于8点呢？是遇到什么困难了嘛 =。=?"
FORMAT_ERROR_REMINDER_COPYWRITE_TEMPLATE = "Hi，[[USER_NAME_PLACEHOLDER]]，昵称识别失败，群里 @Bean 查下哈"

NO_USER_NEED_AT_COPYWRITE_TEMPLATE = '喜大普奔，今日无人可@'

TIME_END_FLAGS = {'\n', '-', '—'}


class ChainMessageReminderService(object):

    def __init__(self, message: Message):
        self._message = message
        self._get_up_content_dict = {}

    @property
    def get_up_content_dict(self):
        return self._get_up_content_dict

    def handle(self, with_get_up_time: bool = False) -> str:
        self._get_up_content_dict, format_error_users = self._parse_get_up_time_and_log()
        if with_get_up_time:
            get_up_time_msg = self._build_get_up_time_msg(self._get_up_content_dict)
        else:
            get_up_time_msg = ''

        unlog_users = self._get_unlog_users(self._get_up_content_dict)
        get_up_late_users = self._get_get_up_late_users(self._get_up_content_dict)

        unlog_reminder_copywrite = self._build_unlog_reminder_copywrite(unlog_users)
        get_up_late_reminder_copywrite = self._build_get_up_late_reminder_copywrite(get_up_late_users)
        format_error_reminder_copywrite = self._build_format_error_reminder_copywrite(format_error_users)

        return self._build_response_msg(
            unlog_reminder_copywrite,
            get_up_late_reminder_copywrite,
            format_error_reminder_copywrite,
            get_up_time_msg,
        )

    def _parse_get_up_time_and_log(self) -> (dict[str, GetUpData], set):
        get_up_content_dict = {}
        format_error_users = set()

        # Parse the beginning number label
        message_content_dict = parse_message_content_without_format(self._message.content)

        # Parse the get up time and get up log
        # If parse failed, put this user into format_error_users set
        for nick, message in message_content_dict.items():
            hour_res = -1
            minute_res = -1
            log_start = len(message)

            hour_start, hour_end, hour_val = parse_first_integer(message)
            if hour_start != -1:
                nick += f' {message[:hour_start]}'
                nick = nick.strip()

                while hour_end < len(message) and message[hour_end] == ' ':
                    hour_end += 1

                if hour_end == len(message):
                    hour_res = hour_val
                    minute_res = 0
                    log_start = hour_end
                else:
                    hour_min_separaion = message[hour_end]
                    if hour_min_separaion in TIME_END_FLAGS:
                        hour_res = hour_val
                        minute_res = 0
                        log_start = hour_end
                    else:
                        minute_start, minute_pos, minute_val = parse_first_integer(message[hour_end+1:].strip())
                        if minute_start == 0:
                            hour_res = hour_val
                            minute_res = minute_val
                            log_start = hour_end + 1 + minute_pos
                        else:
                            hour_res = hour_val
                            minute_res = 0
                            log_start = hour_end

            get_up_time = None
            get_up_log = None
            try:
                get_up_time = time(hour_res, minute_res)
                get_up_log = message[log_start:].strip()
            except Exception:
                logger.error(f'ChainMessageReminderService._parse_get_up_time_and_log error, '
                             f'nick: {nick}, message: {message}')

            # Build GetUpData for current user
            if get_up_time:
                data = GetUpData(nick, get_up_time, get_up_log)
                if nick not in get_up_content_dict \
                        or data.get_up_time < get_up_content_dict[nick].get_up_time:
                    get_up_content_dict[nick] = data
            else:
                format_error_users.add(nick)

        return get_up_content_dict, format_error_users

    @staticmethod
    def _get_unlog_users(get_up_content_dict: dict[str, GetUpData]) -> set:
        unlog_users = set()
        for nick, data in get_up_content_dict.items():
            if len(data.get_up_log) < VALID_LOG_MIN_LEN:
                unlog_users.add(nick)
        return unlog_users

    @staticmethod
    def _get_get_up_late_users(get_up_content_dict: dict[str, GetUpData]) -> set:
        get_up_late_users = set()
        for nick, data in get_up_content_dict.items():
            if GET_UP_LATE_TIME < data.get_up_time:
                get_up_late_users.add(nick)
        return get_up_late_users

    @staticmethod
    def _build_unlog_reminder_copywrite(unlog_users: set) -> str:
        if unlog_users:
            users_str = '@' + ' @'.join(unlog_users)
            return UNLOG_REMINDER_COPYWRITE_TEMPLATE.replace(USER_NAME_PLACEHOLDER, users_str)
        else:
            return ''

    @staticmethod
    def _build_get_up_late_reminder_copywrite(get_up_late_users: set) -> str:
        if get_up_late_users:
            users_str = '@' + ' @'.join(get_up_late_users)
            return GET_UP_LATE_REMINDER_COPYWRITE_TEMPLATE.replace(USER_NAME_PLACEHOLDER, users_str)
        else:
            return ''

    @staticmethod
    def _build_format_error_reminder_copywrite(format_error_users: set) -> str:
        if format_error_users:
            users_str = '@' + ' @'.join(format_error_users)
            return FORMAT_ERROR_REMINDER_COPYWRITE_TEMPLATE.replace(USER_NAME_PLACEHOLDER, users_str)
        else:
            return ''

    @staticmethod
    def _build_get_up_time_msg(get_up_content_dict: dict[str, GetUpData]) -> str:
        get_up_time_arr = []
        for key, val in get_up_content_dict.items():
            get_up_time_arr.append(f'{key} {val.get_up_time.strftime("%H:%M")}')
        if get_up_time_arr:
            return '【大家的起床时间】\n' + '\n'.join(get_up_time_arr)
        else:
            return ''

    @staticmethod
    def _build_response_msg(*args: str) -> str:
        response_msg_arr = []
        for arg in args:
            if arg:
                response_msg_arr.append(arg)

        if response_msg_arr:
            return '\n\n'.join(response_msg_arr)
        else:
            return NO_USER_NEED_AT_COPYWRITE_TEMPLATE
