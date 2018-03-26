from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from bookings import views

urlpatterns = [
    url(r'^bookings/$', views.BookingList.as_view()),
    url(r'^bookings/(?P<pk>[0-9]+)/$', views.BookingDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)