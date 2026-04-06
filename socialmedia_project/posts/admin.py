from django.contrib import admin
from .models import Post, Like, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'category', 'is_flagged', 'flag_reason', 'created_at')
    list_filter = ('is_flagged', 'category')
    search_fields = ('author__username', 'content')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'is_flagged', 'created_at')
    list_filter = ('is_flagged',)