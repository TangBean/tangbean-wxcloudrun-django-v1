from django.conf.urls import url

from .views import MessageDispatcherAPIView


urlpatterns = [
    url(r'^message/?$', MessageDispatcherAPIView.as_view()),
]
