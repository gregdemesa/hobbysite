from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from .models import ArticleCategory, Article, Comment
from .forms import CommentForm, CreateForm, UpdateForm
from user_management.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

def article_list(request):
    user = request.user
    user_articles = Article.objects.filter(author=user).order_by('-created_on')
    other_articles = Article.objects.exclude(author=user).order_by('-created_on')

    combined_articles = list(user_articles) + list(other_articles)

    ctx = {'articles': combined_articles}
    return render(request, 'article_list.html', ctx)

def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    ctx = {'article': article}
    return render(request, 'article_detail.html', ctx)

class ArticleListView(ListView):
    model = Article
    template_name = "article_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            try:
                user_articles = queryset.filter(author=user.profile)
                other_articles = queryset.exclude(author=user.profile)
                return list(user_articles) + list(other_articles)
            except AttributeError:
                return queryset
        else:
            return queryset

class ArticleDetailView(DetailView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user.profile
            comment.created_on = timezone.now()
            comment.save()
            return redirect('wiki:article', pk=self.object.pk)
        else:
            return render(request, self.template_name, {'article': self.object, 'form': form})

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return redirect('wiki:article', pk=self.object.pk)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'article': self.object, 'form': form})


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = CreateForm
    template_name = "article_create.html"
    success_url = reverse_lazy('wiki:articles')

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        form.instance.image = self.request.FILES.get('image')
        form.save()
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = UpdateForm
    template_name = "article_update.html"

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        article = self.get_object()
        article.title = form.cleaned_data['title']
        article.articlecategory = form.cleaned_data['articlecategory']
        article.entry = form.cleaned_data['entry']
        article.created_on = form.cleaned_data['created_on']
        article.image = form.cleaned_data['image']
        article.save()
        return redirect('wiki:article', pk=self.kwargs['pk'])

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

def image_gallery(request):
    articles = Article.objects.all()
    image_urls = []
    for article in articles:
        if article.image:
            image_urls.append(article.image.url)

    return render(request, 'article_gallery.html', {'image_urls': image_urls})
