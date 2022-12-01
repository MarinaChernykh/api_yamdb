from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Review, Comment, Title, SCORE_CHOICES


class ReviewSerializer(serializers.ModelSerializer):
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
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)
