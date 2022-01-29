"""Модуль управления путями для api."""
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet


v1_router = SimpleRouter()
v1_router.register('posts', PostViewSet)
v1_router.register('groups', GroupViewSet)
v1_router.register(
    r'posts/(?P<post_pk>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
v1_router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
