from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from bookings import views

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]