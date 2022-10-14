from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import News, Comment
from .forms import NewsForm, UserRegisterForm, UserLoginForm, CommentForm


class HomeNews(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        return News.objects.filter(is_published=True)


class CreateNews(CreateView):
    form_class = NewsForm

    template_name = 'news/add_news.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        return super(CreateNews, self).form_valid(form)


class ViewNews(FormMixin, DetailView):
    model = News
    context_object_name = 'news_item'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.news = self.get_object()
        self.object.save()
        return super(ViewNews, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'news': self.object})
        context['comment'] = Comment.objects.filter(news=self.object.id)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context

    def get_success_url(self):
        print(self.get_object().slug)
        return reverse_lazy('view_news', kwargs={'slug': self.get_object().slug})


class NewsByCategory(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['slug'],
                                   is_published=True)


class UserNewsByCategory(ListView):
    model = News
    template_name = 'news/user_category.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['slug'],
                                   is_published=True, author=self.request.user.pk)


class UserNews(ListView):
    model = News
    template_name = 'news/user_news.html'
    context_object_name = 'news'
    paginate_by = 0

    def get_queryset(self):
        query = News.objects.filter(author=self.request.user.pk)
        if query:
            self.paginate_by = 3
            return query
        else:
            messages.info(self.request, 'You have not had your own news yet ')


class EditNews(UpdateView):
    model = News
    form_class = NewsForm

    template_name = 'news/user_edit_news.html'


class DeleteNews(DeleteView):
    model = News
    success_url = reverse_lazy('user_news')


class Search(ListView):
    template_name = 'news/search.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        return News.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You successfully registered')
            return redirect('login')
        else:
            messages.error(request, 'Try again')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

