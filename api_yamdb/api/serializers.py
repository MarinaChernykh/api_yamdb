from rest_framework import serializers

from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
            read_only=True,
            slug_field='username'
            )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)
