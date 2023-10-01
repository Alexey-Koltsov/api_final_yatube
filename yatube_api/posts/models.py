from django.contrib.auth import get_user_model
from django.db import models

from .constants import SIMBOLS_QUANTITY

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название группы', max_length=200)
    slug = models.SlugField('Слаг', unique=True)
    description = models.TextField('Описание')

    def __str__(self):
        return self.title[:SIMBOLS_QUANTITY]


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        verbose_name='Группа поста',
        related_name='posts',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:SIMBOLS_QUANTITY]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        default_related_name = 'comments'

    def __str__(self):
        return (f'Для поста {self.post[:SIMBOLS_QUANTITY]}...'
                f' {self.author} комментирует: {self.text[:SIMBOLS_QUANTITY]}')


class Follow(models.Model):
    user = models.ForeignKey(
        User, related_name='following_set', on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, related_name='user_set', on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique-in-module'
            ),
            models.CheckConstraint(
                name='user_prevent_self_follow',
                check=~models.Q(user=models.F('following')),
            ),
        ]

    def __str__(self):
        return (f'{self.user.username} подписан на {self.follow.username}')
