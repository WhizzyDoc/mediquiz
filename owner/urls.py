from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.admin_login, name="admin_login"),
    path('', views.dashboard, name="admin_dashboard"),
    # Users
    path('users/', views.user_list, name="user_list"),
    path('users/<str:username>/account/', views.account_status, name="account_status"),
    path("users/<str:username>/", views.user_detail, name="user_detail"),
    path('users/<str:username>/edit/', views.user_edit, name="user_edit"),
    path('users/<str:username>/delete/', views.user_delete, name="user_delete"),
    # Groups
    path('groups/', views.group_list, name="groups_list"),
]