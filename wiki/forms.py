from django import forms
from .models import Article, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']

class CreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'articlecategory', 'entry', 'image']

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'articlecategory','created_on', 'entry', 'image']
        labels = {
            'articlecategory' : 'Category',
        }
