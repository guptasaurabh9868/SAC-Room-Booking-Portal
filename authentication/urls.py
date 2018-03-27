from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from authentication import views

app_name = 'authentication'

router = DefaultRouter()
router.register(r'accounts', views.AccountViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^auth/login/', views.account_login, name='login'),
    url(r'^auth/signup/', views.account_signup, name='signup'),
    url(r'^auth/logout/', views.account_logout, name='logout'), 
]

