from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью POST."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью Group."""

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью Follow."""

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def get_queryset(self):
        return self.context['request'].user.following_set.all()

    def validate_following(self, value):
        request = self.context['request']
        follows_list = list(self.get_queryset().values_list(
            'following__username', flat=True))
        if value.username == request.user.username:
            raise serializers.ValidationError(
                'Подписываться на самого себя запрещено!'
            )
        if value.username in follows_list:
            raise serializers.ValidationError(
                f'{request.user.username} уже подписан(а)'
                f' на {value.username}!'
            )
        return value
