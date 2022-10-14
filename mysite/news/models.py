from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils.text import slugify
from trans import trans
from ckeditor_uploader.fields import RichTextUploadingField


class News(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(
        max_length=80,
        null=False,
        unique=True)
    content = RichTextUploadingField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(
        upload_to='photos/%d/%m/%Y/',
        blank=True)
    is_published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(trans(self.title))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('view_news', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['created_at', 'is_published']


class Category(models.Model):
    title = models.CharField(
        max_length=150,
        db_index=True)
    slug = models.SlugField(
        max_length=80,
        null=False,
        unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.news.title} - {self.user}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-date_added']