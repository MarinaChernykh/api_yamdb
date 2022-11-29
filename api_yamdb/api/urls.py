from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

router_v1 = routers.DefaultRouter()


urlpatterns = [
    path('v1/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/', include(router_v1.urls)),
]
