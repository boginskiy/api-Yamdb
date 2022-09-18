from django.contrib import admin
from user.models import User
from reviews.models import Genre, Category, Title, Review, Comment

admin.site.register(User)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


admin.site.register(Genre, GenreAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


admin.site.register(Category, CategoryAdmin)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category')


admin.site.register(Title, TitleAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'score', 'pub_date')


admin.site.register(Review, ReviewAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')


admin.site.register(Comment, CommentAdmin)
