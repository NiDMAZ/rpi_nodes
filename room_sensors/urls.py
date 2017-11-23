from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^api/sensors/$', views.api_sensor(), name='api_sensor response'),
]
