from django.conf.urls import url, include
from rooms import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls))
]