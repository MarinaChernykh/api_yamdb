from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins, response
from rest_framework import permissions, status, views
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend

from .filters import FilterForTitle
from .serializers import (GetTokenSerializer, PersSerializer, SingUpSerializer,
                          UsersSerializer, CategorySerializer,
                          GenreSerializer, ReviewSerializer, CommentSerializer,
                          TitleReadSerializer, TitleWriteSerializer)
from reviews.models import User, Title, Category, Genre, Review
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorOrModeratorOrAdminOrReadOnly)


MESSAGE_EMAIL_EXISTS = 'Этот email уже занят'
MESSAGE_USERNAME_EXISTS = 'Это имя уже занято'


class UsersViewSet(viewsets.ModelViewSet):
    """Отображение действий с пользователями."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    search_fields = ('username',)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = PersSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(
                serializer.data, status=status.HTTP_200_OK
            )
        serializer = PersSerializer(user)
        return response.Response(
            serializer.data, status=status.HTTP_200_OK
        )


class SignUp(views.APIView):
    """Функция регистрации новых пользователей."""

    serializer_class = SingUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(
                username=serializer.validated_data.get('username'),
                email=serializer.validated_data.get('email')
            )
        except IntegrityError:
            return response.Response(
                MESSAGE_EMAIL_EXISTS if
                User.objects.filter(username='username').exists()
                else MESSAGE_USERNAME_EXISTS,
                status.HTTP_400_BAD_REQUEST
            )
        code = default_token_generator.make_token(user)
        send_mail(
            'Код токена',
            f'Код для получения токена {code}',
            settings.DEFAULT_FROM_EMAIL,
            [serializer.validated_data.get('email')]
        )
        return response.Response(
            serializer.data, status=status.HTTP_200_OK
        )


@api_view(['POST'])
def get_token(request):
    """Функция получения токена при регистрации."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data.get(
        'confirmation_code'
    )
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return response.Response(
            {'token': str(token)}, status=status.HTTP_200_OK
        )
    return response.Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Отображение действий с категориями произведений."""
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Отображение действий с жанрами для произведений."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Отображение действий с произведениями."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, )
    filterset_class = FilterForTitle
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Отображение действий с отзывами."""
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorOrModeratorOrAdminOrReadOnly,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Отображение действий с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrModeratorOrAdminOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title=self.kwargs['title_id'],
            pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
