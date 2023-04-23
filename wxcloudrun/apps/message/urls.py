from django.conf.urls import url

from .views import MessageDispatcherAPIView


app_name = 'message'
urlpatterns = [
    url(r'^message/?$', MessageDispatcherAPIView.as_view()),
]
