from rest_framework import serializers
from rest_framework.relations import StringRelatedField


from posts.models import Comment, Post, Group, Follow


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
    user = StringRelatedField(read_only=True)
    following = StringRelatedField(read_only=True)

    class Meta:
        fields = ('user', 'following')
        read_only_fields = ('user',)
        model = Follow
