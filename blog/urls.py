from django.urls import path
from .views import CategoryListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView

urlpatterns = [
    path('blog/articles/', CategoryListView.as_view(), name="articlelist"),
    path('blog/article/<int:pk>/', ArticleDetailView.as_view(), name='article'),
    path('blog/article/create/', ArticleCreateView.as_view(), name='blog_create'),
    path('blog/article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='blog_update'),
]

app_name ="blog"

