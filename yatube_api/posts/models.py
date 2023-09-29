from django.contrib.auth import get_user_model
from django.db import models

from .constants import SIMBOLS_QUANTITY

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название группы', max_length=200)
    slug = models.SlugField('Слаг', unique=True)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'Группы'

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
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:SIMBOLS_QUANTITY]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

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

    def __str__(self):
        return self.user.username
