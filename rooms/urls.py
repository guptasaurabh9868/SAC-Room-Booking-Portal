from django.conf.urls import url
from rooms import views

urlpatterns = [
    url(r'^rooms/$', views.room_list),
    url(r'^rooms/(?P<number>[0-9]+)/$', views.room_detail),
]