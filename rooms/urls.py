from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rooms import views

urlpatterns = [
    url(r'^rooms/$', views.RoomList.as_view()),
    url(r'^rooms/(?P<number>[0-9]+)/$', views.RoomDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)