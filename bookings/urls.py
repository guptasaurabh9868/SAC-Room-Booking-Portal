from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from bookings import views

app_name = "bookings"

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^bookings/create/$', views.create_booking, name='create-booking'),
    url(r'^bookings/$', views.show_bookings, name='show-bookings'),       
    url(r'^bookings/delete/(?P<pk>[0-9]+)/', views.delete_booking, name='delete-booking'),
    url(r'^bookings/approve/(?P<pk>[0-9]+)/', views.approve_booking, name='approve-booking'),
    url(r'^bookings/reject/(?P<pk>[0-9]+)/', views.reject_booking, name='reject-booking'),
    url(r'^bookings/conflict/$', views.booking_conflict, name='booking-conflict'),
]