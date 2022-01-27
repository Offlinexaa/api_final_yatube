from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework import permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from posts.models import Post, Group, Follow
from api.serializers import PostSerializer, GroupSerializer, CommentSerializer
from api.serializers import FollowerSerializer
from api.permissions import AuthorOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        serializer.save(post=post, author=self.request.user)


class FollowViewSet(ViewSet):
    def list(self, request):
        queryset = Follow.objects.filter(user=request.user)
        serializer = FollowerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = FollowerSerializer(data=request.data)
        if serializer.is_valid():
        #     serializer.validated_data['user'] = request.user
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
