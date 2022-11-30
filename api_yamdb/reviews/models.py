from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UsernameRegexValidator, username_me

LENG_SLUG = 50
LENG_MAX = 256
LENG_DATA_USER = 150
LENG_EMAIL = 254
LENG_CUT = 30


# Create your models here.
class User(AbstractUser):

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
        max_length=LENG_DATA_USER,
        unique=True,
        blank=False,
        null=False,
        help_text=f'Набор символов не более {LENG_DATA_USER}.'
                  'Только буквы, цифры и @/./+/-/_',
        error_messages={
            'unique': "Пользователь с таким именем уже существует!",
        },
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=LENG_EMAIL,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    REQUIRED_FIELDS = ('email', )
