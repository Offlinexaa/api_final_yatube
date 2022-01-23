from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import GroupViewSet, PostViewSet


v1_router = SimpleRouter()
v1_router.register('posts', PostViewSet)
v1_router.register('groups', GroupViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
]
