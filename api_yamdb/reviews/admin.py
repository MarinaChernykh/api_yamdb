from django.contrib import admin
from .models import Review, Comment


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text','author', 'score', 'pub_date', 'title')
    search_fields = ('title', 'text')
    list_filter = ('pub_date', 'score')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text','author', 'pub_date', 'review')
    search_fields = ('review', 'text')
    list_filter = ('pub_date',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
