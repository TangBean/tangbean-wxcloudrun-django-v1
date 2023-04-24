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


if __name__ == '__main__':
    content_data_0 = '#接龙\n这就自己干！\n4.24\n\n1. 齐格 在写 微信群接龙 Report Generation Feature，完成情况如下：\n* 设计数据库结构 ，创建了一个表，project的表还没创建\n* 写入消息功能，还没往数据库写，还有日期 project解析功能需要开发\n* 收到消息回复是否写入成功功能：验证了可以通过被动消息回复用户\n* 昨天调环境调了好久，麻蛋把数据库密码改了自己给忘了。。\n2. 颜泱 1. 尝试了一下把unity代码传入github。为5.1异地继续课程做准备。2. 肝工作，第二个任务拿到了一些优化。3. 使用更详细的条件让chatgpt帮忙生成自动地图，还没测试\n3. Saltyfish 1.把上次视频9的实现完成了 2.看qige写的文档'
    content_data_1 = '#补充接龙信息\n这就自己干！'
    content_data_2 = '#新建接龙项目\n这就自己干！'
    content_data_3 = '#生成接龙报告\n这就自己干！'
    content_data_4 = '#哈哈哈哈哈\n这就自己干！'
    content_data_5 = '哈哈哈哈哈\n这就自己干！'
    print(parse_message_biz_type(content_data_0))
    print(parse_message_biz_type(content_data_1))
    print(parse_message_biz_type(content_data_2))
    print(parse_message_biz_type(content_data_3))
    print(parse_message_biz_type(content_data_4))
    print(parse_message_biz_type(content_data_5))
