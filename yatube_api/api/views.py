from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Comment, Group, Post


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """
    Получаем список всех постов или создаем новый пост.
    Получаем, редактируем или удаляем пост по id.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получаем список всех групп или создаем новую группу.
    Получаем, редактируем или удаляем группу по id.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получаем список всех всех комментариев поста с id=post_id или
    создаём новый, указав id поста, который хотим прокомментировать.
    Получаем, редактируем или удаляем комментарий по id у поста с id=post_id.
    """

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]

    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        return Comment.objects.filter(post=self.get_post())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post=self.get_post())


class FollowList(generics.ListCreateAPIView):
    """
    Получаем список всех авторов на кого подписан пользователь.
    Добавляем подписку для пользователя по username.
    """

    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        return self.request.user.following_set.all()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        follows_list = list(self.get_queryset().values_list(
            'following__username', flat=True))
        if 'following' not in request.data.keys():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.data['following'] == request.user.username:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.data['following'] in follows_list:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)
