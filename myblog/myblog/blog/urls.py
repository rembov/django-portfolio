from django.urls import path
from . import views
from .feeds import LatestPostsFeed

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('rss/', LatestPostsFeed(), name='rss_feed'),
]