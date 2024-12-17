from django.db import models
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from user_management.models import Profile

class ArticleCategory(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()

	def get_absolute_url(self):
		return reverse('wiki:category', kwargs={'pk': self.pk})


	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-name']

class Article(models.Model):
	title = models.CharField(max_length=255)
	author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
	articlecategory = models.ForeignKey('ArticleCategory', on_delete=models.CASCADE, null=True)
	entry = models.TextField()
	image = models.ImageField(upload_to = 'images/', null=True)
	created_on = models.DateTimeField(default=datetime.now, blank=True)
	updated_on = models.DateTimeField(auto_now=True)

	def get_absolute_url(self):
		return reverse('wiki:article', kwargs={'pk': self.pk})

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-articlecategory__name', '-created_on']

class Comment(models.Model):
	author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=False)
	article = models.ForeignKey(Article, on_delete=models.CASCADE)
	entry = models.TextField()
	created_on = models.DateTimeField(default=datetime.now, blank=True)
	updated_on = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.entry

	class Meta:
		ordering = ['-created_on']
