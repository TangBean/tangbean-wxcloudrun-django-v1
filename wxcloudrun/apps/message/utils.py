from enum import Enum


class MessageBizType(Enum):
    CHAIN_MSG = '#接龙'
    MAKE_UP_CHAIN_MSG = '#补充接龙信息'
    NEW_CHAIN_PROJECT_MSG = '#新建接龙项目'
    GEN_REPORT_MSG = '#生成接龙报告'
    UNKNOWN_MSG = '#未知消息类型'


def parse_message_biz_type(content: str) -> MessageBizType:
    message_type = ''
    for c in content:
        if c == '\n' or c == ' ':
            break
        message_type += c
    return MessageBizType._value2member_map_.get(message_type, MessageBizType.UNKNOWN_MSG)
