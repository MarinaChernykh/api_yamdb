from datetime import datetime as dt
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import (Review, Comment, Title,
                            Category, Genre, User,
                            username_me, SCORE_CHOICES)
from reviews.validators import UsernameRegexValidator


class SingUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UsernameRegexValidator(), ]
    )

    def validate_username(self, value):
        return username_me(value)


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена при регистрации."""

    username = serializers.CharField(
        required=True,
        validators=(UsernameRegexValidator(), )
    )
    confirmation_code = serializers.CharField(required=True)

    def validate_username(self, value):
        return username_me(value)


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для новых юзеров."""

    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            UsernameRegexValidator()
        ]
    )

    class Meta:
        abstract = True
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class PersSerializer(UsersSerializer):
    """Сериализатор для пользователя."""

    class Meta(UsersSerializer.Meta):
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для работы с категориями."""
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с жанрами."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.ChoiceField(choices=SCORE_CHOICES)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title',)

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title = get_object_or_404(
                Title, id=self.context['view'].kwargs['title_id'])
            author = request.user
            if title.reviews.filter(author=author).exists():
                raise serializers.ValidationError(
                    'Вы не можете оставить отзыв повторно!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с комментариями."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для возврата списка произведений."""

    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    rating = serializers.IntegerField(required=False)
    # year = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    # def to_representation(self, instance):
    #     return TitleReadSerializer(instance).data

    def validate_year(self, data):
        if data >= dt.now().year:
            raise serializers.ValidationError(
                f'Год {data} больше текущего!',
            )
        return data
    
    # def validate_year(self, value):                       # Почему не работает???????
    #     year = dt.date.today().year
    #     if value > year:
    #         raise serializers.ValidationError(
    #             'Год выпуска не может быть больше текущего!'
    #         )
    #     return value