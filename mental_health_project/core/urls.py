from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('survey/', views.survey, name='survey'),
    path('results/<int:response_id>/', views.results, name='results'),
    path('history/', views.history, name='history'),
    path('authors/', views.authors, name='authors'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # User Management
    path('users/', views.user_management, name='user_management'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/toggle-role/<int:user_id>/', views.toggle_user_role, name='toggle_user_role'),
]
