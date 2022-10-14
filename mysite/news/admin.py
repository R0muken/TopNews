from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import News, Category, Comment


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'category', 'updated_at', 'is_published', 'get_photo', 'views')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    readonly_fields = ('views',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="60">')
        return '-'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title')
    list_display_links = ('title',)
    search_fields = ('title',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
