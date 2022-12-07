from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UsernameRegexValidator, username_me
from api_yamdb.settings import AUTH_USER_MODEL
from core.models import CommentsAndReviews, CategoryAndGenre


SCORE_CHOICES = (
    (1, '1 - Отвратительно'),
    (2, '2 - Очень плохо'),
    (3, '3 - Плохо'),
    (4, '4 - Скорее плохо'),
    (5, '5 - Средне'),
    (6, '6 - Неплохо'),
    (7, '7 - Скорее хорошо'),
    (8, '8 - Хорошо'),
    (9, '9 - Очень хорошо'),
    (10, '10 - Великолепно')
)


class User(AbstractUser):
    """Содержит данные о пользователях."""

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    )

    username = models.CharField(
        'Имя пользователя',
        validators=(UsernameRegexValidator(), username_me),
        max_length=150,
        unique=True,
        blank=False,
        help_text='Только буквы, цифры и @/./+/-/_',
        error_messages={
            'unique': 'Пользователь с таким именем уже существует!',
        },
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
    )
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email',
            )
        ]

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    def __str__(self):
        return f'{self.username} {self.email} {self.role}'


class Category(CategoryAndGenre):
    """Содержит данные о категориях произведений."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryAndGenre):
    """Содержит данные о жанрах произведений."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Содержит данные о произведениях."""
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год создания', )
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        null=True,
        blank=True,
        through='TitleGenre',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year',)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Служит для обеспечения связей многие-ко-многим."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(CommentsAndReviews):
    """Содержит пользовательские отзывы о произведениях."""
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField('Оценка', choices=SCORE_CHOICES)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]


class Comment(CommentsAndReviews):
    """Содержит комментарии о произведениях."""
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
