from django.contrib import admin

from .models import Book, Subscription, Tag, Genre, Like


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'subscription_type')
    list_filter = ('id', 'title', 'author', 'subscription_type')
    search_fields = ('id', 'title', 'author', 'subscription_type')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'user', 'duration', 'start_date')
    list_filter = ('id', 'type', 'duration', 'start_date')
    search_fields = ('id', 'type', 'duration', 'start_date')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_filter = ('id', 'title',)
    search_fields = ('id', 'title',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_filter = ('id', 'title',)
    search_fields = ('id', 'title',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user')
    list_filter = ('id',)
    search_fields = ('id',)
