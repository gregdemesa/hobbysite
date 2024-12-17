from django.contrib import admin
from .models import ArticleCategory, Article, Comment

class ArticleInline(admin.TabularInline):
    model = Article

class ArticleAdmin(admin.ModelAdmin):
    model = Article
    inlines = [ArticleInline]

class CommentAdmin(admin.ModelAdmin):
    model = Comment

admin.site.register(ArticleCategory, ArticleAdmin)
admin.site.register(Article)
admin.site.register(Comment)
