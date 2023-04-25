from django.test import TestCase

from wxcloudrun.apps.message.domain.chain_message.chain_message_service import ChainMsgService
from wxcloudrun.apps.message.models import Message


class ChainMsgServiceTest(TestCase):
    test_msgs = [
        '#接龙\n这就自己干！\n4.24\n\n1. 齐格 在写 微信群接龙 Report Generation Feature，完成情况如下：\n* 设计数据库结构 ，创建了一个表，project的表还没创建\n* 写入消息功能，还没往数据库写，还有日期 project解析功能需要开发\n* 收到消息回复是否写入成功功能：验证了可以通过被动消息回复用户\n* 昨天调环境调了好久，麻蛋把数据库密码改了自己给忘了。。\n2. 颜泱 1. 尝试了一下把unity代码传入github。为5.1异地继续课程做准备。2. 肝工作，第二个任务拿到了一些优化。3. 使用更详细的条件让chatgpt帮忙生成自动地图，还没测试\n3. Saltyfish 1.把上次视频9的实现完成了 2.看qige写的文档',
        '#接龙\n例 5；03\n\n1. 吃可爱长大的🐑\n2. 吃可爱长大的🐑5:00-5:30洗漱，出门\n3. 00-5:30洗漱，出门\n4. 琴子 Miyo 5:30 5:30-6:00洗漱收拾 6:30-8:00赶飞机\n5. 刘畅 5:55\n- 6:30 扣手机，微信阅读\n- 7:00 健身\n- 7: 40 做饭，洗漱\n- 9: 15 算法题\n6. Bean 6\n-7:30 出门健身房跑步回家\n-7:50 早饭 & 微信读书\n-8:20 毫无意义的刷手机\n-8:50 在滴答清单里列最近想实现的一个feature的task list\n7. 大京-上海 6:30\n-6:45刷手机\n-7:55洗漱早餐赶路\n-8:20投资理财\n-9:00学习腹部肌肉解剖\n8. Y.jun 6.30\n6.30-6.50揉肚子称体重喝水\n6.50-7.30扣手机研究抗炎食物\n7.30-7.55薄荷原著\n7.55-8.30收拾出门\n9. 丁达尔效应 7\n-7.30 整理东西\n-8.20 洗漱化妆\n-9.00 看漫画\n10. 大螃蟹 7-8:40\n-8:00 补觉\n-8:40 洗漱收拾，晾衣服\n11. 影妹 7:10\n7:10 -8:00 学习备考视频+keep\n出门\n12. W 7:20-8:30洗漱吃早餐化妆换衣服\n8:30-9:20玩手机闭目养神\n9:20-9:40通勤上班\n13. 和尚 7.40-9.30\u2028-8.32 扣手机洗漱咖啡\u2028-9.31 写点碎碎念（突然意识到，为什么我可以这么能叭叭叭，写这么久）\u2028-9.38 准备早餐\n14. Shen 7.30\n15. 冰风陌 6.35 6.35-6.55洗漱，6.55-7.05煮水喝水，7.05-8.35看教学视频，8.35-8.50收拾上班\n16. XQian 6:30躺着-7:00洗头发-8:20吃饭收拾-9:20看动画-9:42通勤',
    ]
    for test_msg in test_msgs:
        message = Message(
            msg_id='MsgId',
            msg_type='MsgType',
            to_user_name='ToUserName',
            from_user_name='FromUserName',
            create_time='CreateTime',
            content=test_msg,
        )
        service = ChainMsgService(message)
        project_message = service.parse_project_message()
        service.parse_message_content()
        print(project_message)
        print(service.message.content)
