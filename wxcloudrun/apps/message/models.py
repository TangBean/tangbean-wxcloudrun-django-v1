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


class Message(object):

    def __init__(self, msg_id, to_user_name, from_user_name, create_time, msg_type, content):
        self.msg_id = msg_id
        self.msg_type = msg_type
        self.to_user_name = to_user_name
        self.from_user_name = from_user_name
        self.create_time = create_time
        self.content = content


class ChainMessageDaily(models.Model):
    id = models.AutoField
    created_time = models.DateTimeField(default=datetime.now(), )
    updated_time = models.DateTimeField(default=datetime.now(), )
    content = models.TextField()
    to_user_name = models.CharField(max_length=64, )
    from_user_name = models.CharField(max_length=64, )
    msg_id = models.BigIntegerField(max_length=32, )
    message_time = models.BigIntegerField(max_length=32, )
    project_name = models.CharField(max_length=128, )
    msg_date = models.DateTimeField()

    def __str__(self):
        return f'{self.project_name}-{self.msg_id}-{self.message_time}: {self.content}'

    class Meta:
        db_table = 'chain_message_daily'


class ChainProject(models.Model):
    id = models.AutoField
    project_name = models.CharField(max_length=128, )
    creator = models.CharField(max_length=64, )
    created_time = models.DateTimeField(default=datetime.now(), )
    updated_time = models.DateTimeField(default=datetime.now(), )

    def __str__(self):
        return f'{self.id}-{self.project_name}-{self.creator}'

    class Meta:
        db_table = 'chain_project'
