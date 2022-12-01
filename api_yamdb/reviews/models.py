from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

SCORE_CHOICES = (
    (1, '1'), (2, '2'), (3, '3'),
    (4, '4'), (5, '5'), (6, '6'),
    (7, '7'), (8, '8'), (9, '9'),
    (10, '10')
    )


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre, through='TitleGenre',
        related_name='titles'
    )

    def __str__(self):
        return self.title


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')

    def __str__(self):
        return self.text

