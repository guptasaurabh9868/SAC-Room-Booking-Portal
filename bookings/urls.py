from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from bookings import views

app_name = "bookings"

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^bookings/create', views.create_booking, name='create-booking'),
    url(r'^bookings/', views.show_bookings, name='show-bookings'),       
]