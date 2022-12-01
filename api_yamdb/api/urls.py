from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, CategoryViewSet, GenreViewSet, ReviewViewSet, CommentViewSet


app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('titles', TitleViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register(
    r'titles/(?P<title_id>[1-9]\d*)/reviews',
    ReviewViewSet, basename='reviews'
    )
router_v1.register(
    r'titles/(?P<title_id>[1-9]\d*)/reviews/(?P<review_id>[1-9]\d*)/comments',
    CommentViewSet, basename='comments'
    )

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
