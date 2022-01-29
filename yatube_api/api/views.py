from rest_framework import filters, mixins, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)

from api.permissions import AuthorOrReadOnly
from api.serializers import (CommentSerializer, FollowerSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Group, Post


class PostViewSet(ModelViewSet):
    """
    Вьюсет для модели Post.
    Включена паджинация.
    Права: автору можно всё, остальным - только чтение.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """
        Создание экземпляра модели Post.
        Автором назначается пользователь, сделавший запрос.
        """
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет для модели Group.
    Создание и модификация экземпляров модели не допускается.
    Права: чтение разрешено всем.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(ModelViewSet):
    """
    Вьюсет для модели Comment.
    Права: автору можно всё, остальным - только чтение.
    """
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        """
        Получение набора комментариев к посту указанному в пути запроса.
        Если экземпляра модели Post с казанным pk нет, то возвращаем
        ошибку 404.
        """
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        return post.comments

    def perform_create(self, serializer):
        """
        Создание экземпляра модели Comment.
        Пост назначается по id из пути запроса.
        Автором назначается пользователь, сделавший запрос.
        """
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        serializer.save(post=post, author=self.request.user)


class ListCreateViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    """
    Базовый класс для модели Follow. Выполняет операции получения списка
    объектов и создания объекта.
    """
    pass


class FollowViewSet(ListCreateViewSet):
    """
    Вьюсет для модели Comment.
    Права: только для аутентифицированных пользователей.
    Включен поиск по полю following.
    """
    serializer_class = FollowerSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Получение набора подписок текущего пользователя."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """
        Создание экземпляра модели Follow.
        Подписывается текущий авторизованный пользователь.
        """
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(
                serializer.validated_data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
