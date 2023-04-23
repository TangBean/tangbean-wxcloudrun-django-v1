from django.apps import AppConfig


class MessageAppConfig(AppConfig):
    name = 'wxcloudrun.apps.message'
    label = 'message'
    verbose_name = 'Message'

    def ready(self):
        pass


default_app_config = 'wxcloudrun.apps.message.MessageAppConfig'
