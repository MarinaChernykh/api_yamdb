from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

SCORE_CHOICES = (
    (1, '1'), (2, '2'), (3, '3'),
    (4, '4'), (5, '5'), (6, '6'),
    (7, '7'), (8, '8'), (9, '9'),
    (10, '10')
    )


class Title(models.Model):
    pass


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
