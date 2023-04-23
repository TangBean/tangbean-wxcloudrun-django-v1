from django.apps import AppConfig


class MessageAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wxcloudrun.apps.message'
    label = 'message'
    verbose_name = 'Message'

    def ready(self):
        pass


default_app_config = 'wxcloudrun.apps.message.MessageAppConfig'
