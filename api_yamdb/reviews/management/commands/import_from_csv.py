import csv

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from ...models import (User, Category, Genre,
                       Title, TitleGenre, Review, Comment)


class Command(BaseCommand):
    def handle(self, **options):
        User.objects.all().delete()
        Category.objects.all().delete()
        Genre.objects.all().delete()
        Title.objects.all().delete()
        TitleGenre.objects.all().delete()
        Review.objects.all().delete()
        Comment.objects.all().delete()
        with open(r'static\data\users.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                User.objects.get_or_create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                )
        with open(r'static\data\category.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Category.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
        with open(r'static\data\genre.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Genre.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
        with open(r'static\data\titles.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Title.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=get_object_or_404(Category, pk=row[3])
                )
        with open(r'static\data\genre_title.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                TitleGenre.objects.get_or_create(
                    id=row[0],
                    title=get_object_or_404(Title, pk=row[1]),
                    genre=get_object_or_404(Genre, pk=row[2]),
                )
        with open(r'static\data\review.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Review.objects.get_or_create(
                    id=row[0],
                    title=get_object_or_404(Title, pk=row[1]),
                    text=row[2],
                    author=get_object_or_404(User, pk=row[3]),
                    score=row[4],
                    pub_date=row[5],
                )
        with open(r'static\data\comments.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Comment.objects.get_or_create(
                    id=row[0],
                    review=get_object_or_404(Review, pk=row[1]),
                    text=row[2],
                    author=get_object_or_404(User, pk=row[3]),
                    pub_date=row[4],
                )
