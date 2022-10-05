from django.contrib import admin

from .models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_private')
    list_filter = ('id', 'username', 'email', 'is_private')
    search_fields = ('id', 'username', 'email', 'is_private')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author',)
    list_filter = ('id', 'user', 'author',)
    search_fields = ('id', 'user', 'author',)
