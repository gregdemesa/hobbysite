from django.contrib import admin
from .models import Article, ArticleCategory, Comment

class ArticleInline(admin.TabularInline):
    model = Article

class ArticleAdmin(admin.ModelAdmin):
    model = ArticleCategory
    inlines = [ArticleInline]


class CommentAdmin(admin.ModelAdmin):
    model=  Comment

    
# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(ArticleCategory, ArticleAdmin)
