from django.db import models
from django.conf import settings
from user_management.models import Profile
from django.urls import reverse
from datetime import datetime

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'pk':self.pk})

class Article(models.Model):
    title = models.CharField(max_length=255)
    author =  models.ForeignKey(Profile, related_name='author', on_delete=models.SET_NULL, null=True, blank =True)
    category = models.ForeignKey('ArticleCategory',  related_name='category',on_delete=models.CASCADE, null=True)
    entry = models.TextField()
    header_image = models.ImageField(upload_to='images/', null=True)
    created_on = models.DateTimeField(default= datetime.now, blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category__name','-created_on'] 

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:article', kwargs={'pk':self.pk})


class Comment(models.Model):
    author =  models.ForeignKey(Profile, related_name='commentauthor',on_delete=models.SET_NULL, null=True, blank=False)
    article = models.ForeignKey(Article, related_name='article', on_delete=models.CASCADE, null=True)
    entry = models.TextField()
    created_on = models.DateTimeField(default= datetime.now, blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self) -> str:
        return self.entry
