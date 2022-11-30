from django.urls import include, path

from rest_framework.routers import DefaultRouter
from .views import TitleViewSet, CategoryViewSet, GenreViewSet


v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
