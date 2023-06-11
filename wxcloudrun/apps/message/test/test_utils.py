from django.test import TestCase

from wxcloudrun.apps.message.utils import parse_first_integer


def test_parse_first_integer(message_str):
    start_pos, end_pos, first_num = parse_first_integer(message_str)
    print(message_str)
    print(start_pos, end_pos, first_num)
    print('-------------------')


class UtilsTest(TestCase):
    message_strs = [
        "Miyo  6.35  6.40-7.20听力 7.25-7.35冥想🧘‍♀️ 7.40-8.15洗漱收拾出门\n",
        "35  6.40-7.20听力 7.25-7.35冥想🧘‍♀️ 7.40-8.15洗漱收拾出门\n",
        "8.45今天头疼赖床了。9.30出门门上班",
        "7点55",
        "8.0�-9.40 收拾洗漱上厕所查东西�-10.00 到公司吃早餐准备开始工作",
        "7-8:15洗头发吃早饭化妆收拾-9:10学习-9:20收拾东西-9:50通勤",
        "-7-7:23洗漱",
        "6:16\n-06:30【主业】回工作消息\n-07:10【生活】洗漱 塞尔达\n-07:28【主业】回工作消息\n-08:04【副业】Youtube听写\n-09:05【生活】通勤+复习不背单词+继续看Makudo的视频\n-09:17【生活】吃早饭\n-09:38【生活】昨日总结+今日计划+吐槽\n"
    ]
    for msg in message_strs:
        test_parse_first_integer(msg)
