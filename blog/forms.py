from django import forms
from .models import Article, Comment

class CreateBlog(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'entry', 'category', 'header_image']
        labels = {
            'title': 'Title',
            'category': 'Category',
            'entry': 'Entry',
            'header_image':'Header Image',
        }

class UpdateBlog(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'entry', 'category', 'header_image', 'created_on' ]
        labels = {
            'title': 'Title',
            'category': 'Category',
            'entry': 'Entry',
            'header_image':'Header Image',
            'created_on':'Created On',
        }

class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']
        labels = {
            'entry': 'Entry',
           
        }
