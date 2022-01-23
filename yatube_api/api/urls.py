from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import GroupViewSet, PostViewSet, CommentViewSet


v1_router = SimpleRouter()
v1_router.register('posts', PostViewSet)
v1_router.register('groups', GroupViewSet)
v1_router.register(
    r'posts/(?P<post_pk>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
