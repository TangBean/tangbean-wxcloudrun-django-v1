from datetime import datetime

from django.db import models


# Create your models here.
class Counters(models.Model):
    id = models.AutoField
    count = models.IntegerField(max_length=11, default=0)
    createdAt = models.DateTimeField(default=datetime.now(), )
    updatedAt = models.DateTimeField(default=datetime.now(),)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Counters'  # 数据库表名


class ChainMessageDaily(models.Model):
    id = models.AutoField
    created_time = models.DateTimeField(default=datetime.now(), )
    updated_time = models.DateTimeField(default=datetime.now(), )
    content = models.TextField
    to_user_name = models.CharField(max_length=64, )
    from_user_name = models.CharField(max_length=64, )
    msg_id = models.IntegerField(max_length=32, )
    message_time = models.IntegerField(max_length=32, )
    project_name = models.CharField(max_length=128, )
    msg_date = models.DateTimeField

    def __str__(self):
        return f'{self.project_name}-{self.msg_id}-{self.message_time}: {self.content}'

    class Meta:
        db_table = 'chain_message_daily'
