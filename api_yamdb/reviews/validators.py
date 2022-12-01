from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


LENG_DATA_USER = 150


class UsernameRegexValidator(UnicodeUsernameValidator):
    """Валидация имени пользователя."""

    regex = r'^[\w.@+-]+\Z'
    flags = 0
    max_length = LENG_DATA_USER
    message = (f'Введите правильное имя пользователя. Оно может содержать'
               f' только буквы, цифры и знаки @/./+/-/_.'
               f' Длина не более {LENG_DATA_USER} символов')
    error_messages = {
        'invalid': f'Набор символов не более {LENG_DATA_USER}. '
                   'Только буквы, цифры и @/./+/-/_',
        'required': 'Поле не может быть пустым',
    }


def username_me(value):
    """Проверка имени пользователя (me недопустимое имя)."""
    if value == 'me':
        raise ValidationError(
            'Имя пользователя "me" не разрешено.'
        )
    return value
