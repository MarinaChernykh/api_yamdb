from django.urls import include, path
from rest_framework import routers
from .views import get_token, SignUp


router_v1 = routers.DefaultRouter()


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
