from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleCreateView, image_gallery

urlpatterns = [
    path('wiki/articles/', ArticleListView.as_view(), name='articles'),
    path('wiki/article/<int:pk>', ArticleDetailView.as_view(), name='article'),
    path('wiki/article/<int:pk>/edit', ArticleUpdateView.as_view(), name='article_update'),
    path('wiki/article/add', ArticleCreateView.as_view(), name="article_add"),
    path('wiki/gallery', image_gallery, name='article_gallery'),
]

app_name = 'wiki'
