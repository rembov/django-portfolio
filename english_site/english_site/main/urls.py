from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('words/', views.words_view, name='words'),
    path('game/', views.game_view, name='game'),
    path('grammar/', views.grammar_view, name='grammar'),
    path('speaking/', views.speaking_view, name='speaking'),
    path('awards/', views.awards_view, name='awards'),
    path('check_answer/', views.check_answer, name='check_answer'),
    # Авторизация
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]