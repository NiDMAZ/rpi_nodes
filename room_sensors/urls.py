from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^api/sensors/$', views.api_sensor, name='api_sensor response'),
    url(r'^api/sensors/historical/$', views.api_sensor_historical, name='api_sensor history'),
]
