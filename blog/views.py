from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import CreateBlog,UpdateBlog, CreateComment
from .models import Article
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone



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


class CategoryListView(ListView):
    model = Article
    template_name = "blog_list.html"
    context_object_name = 'articles'
    
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
    form_class = CreateComment
    template_name = "blog_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CreateComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user.profile
            comment.created_on = timezone.now()
            comment.save()
            return redirect('blog:article', pk=self.object.pk)
        else:
            return render(request, self.template_name, {'article': self.object, 'form': form})

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return redirect('blog:articlelist', pk=self.object.pk)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'article': self.object, 'form': form})

class ArticleCreateView (LoginRequiredMixin,CreateView):
    model = Article
    form_class = CreateBlog
    template_name = "blog_create.html"
    success_url = reverse_lazy('blog:articlelist')

    def form_valid(self, form):       
        form.instance.author = self.request.user.profile        
        form.instance.header_image = self.request.FILES.get('header_image')
        form.save()
        return super().form_valid(form)


class ArticleUpdateView (UpdateView):
    model = Article
    form_class = UpdateBlog
    list = Article.objects.all()
    template_name = "blog_update.html"

 
    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        article = self.get_object()
        article.title = form.cleaned_data['title']
        article.category = form.cleaned_data['category']
        article.entry = form.cleaned_data['entry']
        article.created_on = form.cleaned_data['created_on']
        article.header_image = form.cleaned_data['header_image']
        article.save()
        return redirect('blog:article', pk=self.kwargs['pk'])

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))