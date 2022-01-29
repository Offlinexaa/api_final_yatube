from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions, mixins, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from posts.models import Post, Group, Follow, User
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


class ListCreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        GenericViewSet):
    pass


class FollowViewSet(ListCreateViewSet):
    serializer_class = FollowerSerializer

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            if serializer.validated_data['following'] == self.request.user:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                exception=True)
            serializer.validated_data['user'] = self.request.user
            serializer.save()
        return Response(
            data=Follow.objects.last(),
            status=status.HTTP_201_CREATED
        )
