from rest_framework import serializers
from rest_framework.relations import StringRelatedField, SlugRelatedField

from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowerSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(read_only=True, slug_field='username')
    following = SlugRelatedField(
        read_only=False,
        slug_field='username',
        required=True,
        queryset=User.objects.all()
    )

    def validate(self, data):
        user = self.context['request'].user
        if data['following'] == user:
            raise serializers.ValidationError(
                {'following': 'Нельзя подписаться на себя.'}
            )
        if Follow.objects.filter(
            user=user,
            following=data['following']
        ).exists():
            raise serializers.ValidationError(
                {'following': 'Нельзя подписаться на автора повторно.'}
            )
        return data

    class Meta:
        fields = ('user', 'following')
        read_only_fields = ('user',)
        model = Follow
