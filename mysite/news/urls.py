from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeNews.as_view(), name='home'),
    path('category/<str:slug>/', NewsByCategory.as_view(), name='category'),
    path('my-news/category/<str:slug>/', UserNewsByCategory.as_view(), name='usercategory'),
    path('news/<str:slug>/', ViewNews.as_view(), name='view_news'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('my-news/', UserNews.as_view(), name='user_news'),
    path('add-news/', CreateNews.as_view(), name='add_news'),
    path('news/<str:slug>/edit', EditNews.as_view(), name='edit_news'),
    path('news/<str:slug>/delete', DeleteNews.as_view(), name='delete_news'),
    path('search/', Search.as_view(), name='search'),
]