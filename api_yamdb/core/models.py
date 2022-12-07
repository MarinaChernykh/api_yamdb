from django.db import models


class CommentsAndReviews(models.Model):
    """Абстрактный класс для моделей Отзывов и Комментариев."""
    text = models.TextField('Текст',)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class CategoryAndGenre(models.Model):
    """Абстрактный класс для моделей Категорий и Жанров."""
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name
