from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('privacy-policy/', views.privacy, name="privacy"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("groups/", views.group_list, name="group_list"),
    path("groups/<slug:slug>/", views.group_detail, name="group_detail"),
    path("quizzes/", views.quiz_list, name="quiz_list"),
    path("quizzes/<slug:slug>/", views.quiz_detail, name="quiz_detail"),
    path("people/", views.people, name="people"),
    path("people/<str:username>/", views.user_profile, name="user_profile"),

]