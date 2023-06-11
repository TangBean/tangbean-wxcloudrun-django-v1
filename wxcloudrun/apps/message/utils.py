import json
from enum import Enum


class MessageBizType(Enum):
    CHAIN_MSG = '#接龙'
    MAKE_UP_CHAIN_MSG = '#补充接龙信息'
    NEW_CHAIN_PROJECT_MSG = '#新建接龙项目'
    GEN_REPORT_MSG = '#生成接龙报告'
    CHAIN_MSG_REMINDER = '#at'  # 早起群 at
    CHAIN_MSG_REMINDER_LOG = '#atlog'  # 早起群 at with get up time
    UNKNOWN_MSG = '#未知消息类型'


def parse_message_biz_type(content: str) -> MessageBizType:
    message_type = ''
    for c in content:
        if c == '\n' or c == ' ':
            break
        message_type += c
    return MessageBizType._value2member_map_.get(message_type, MessageBizType.UNKNOWN_MSG)


def parse_message_content(message_content):
    res_dict = {}
    msg_content = message_content
    index = 1
    index_label = '1. '
    while True:
        msg_content = msg_content[len(index_label):].strip()
        index = index + 1
        index_label = f'\n{index}. '
        pos = msg_content.find(index_label)
        if pos == -1:
            single_record = msg_content
        else:
            single_record = msg_content[:pos]
            msg_content = msg_content[pos:]

        space_pos = single_record.find(' ')
        if space_pos == -1:
            continue
        key = single_record[:space_pos]
        val = single_record[space_pos+1:].strip()
        res_dict[key] = val.replace('\n', ' ')

        if pos == -1:
            break

    return res_dict


def parse_message_content_without_format(message_content):
    res_dict = {}
    msg_content = message_content
    index = 1
    index_label = '\n1. '
    # Clean up message head
    pos = msg_content.find(index_label)
    if pos == -1:
        return res_dict
    msg_content = msg_content[pos:]

    # Parse message
    while True:
        msg_content = msg_content[len(index_label):]
        index = index + 1
        index_label = f'\n{index}. '
        pos = msg_content.find(index_label)
        if pos == -1:
            single_record = msg_content
        else:
            single_record = msg_content[:pos]
            msg_content = msg_content[pos:]

        space_pos = single_record.find(' ')
        if space_pos == -1:
            continue
        key = single_record[:space_pos]
        val = single_record[space_pos+1:]
        if key in res_dict:
            res_dict[key] += '\n' + val
        else:
            res_dict[key] = val

        if pos == -1:
            break

    return res_dict


def parse_first_integer(message_str) -> (int, int, int):
    """
    Return: (start_pos, end_pos, first_num)
    start_pos: The start pos of the first integer in the message_str
    end_pos: The end pos of the first integer in the message_str
    first_num: The vaule of the first integer in the message_str
    """
    start_pos: int = -1
    end_pos: int = -1
    first_num: int = 0

    find_num = False
    i = 0
    while i < len(message_str):
        c = message_str[i]
        if '0' <= c <= '9':
            if not find_num:
                start_pos = i
            c_num = int(c) - int('0')
            first_num = first_num * 10 + c_num
            find_num = True
        else:
            if find_num:
                break
        i += 1
    if find_num:
        end_pos = i
    return start_pos, end_pos, first_num
