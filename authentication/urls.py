from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from authentication import views

router = DefaultRouter()
router.register(r'accounts', views.AccountViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls))
]

