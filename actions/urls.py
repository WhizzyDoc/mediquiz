from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.activity, name="notifications"),
    path('join/', views.join_group, name="join_group"),
    path('delete-quiz/', views.delete_quiz, name="delete_quiz"),
    path('<slug:slug>/group-quiz/', views.group_quiz, name="group_quiz"),
    path('<slug:slug>/quiz-rank/', views.quiz_rank, name="quiz_rank"),
    path('<slug:slug>/quiz-submit/', views.submit_quiz, name="submit_quiz"),
    path('<slug:slug>/get-questions/<int:order>/', views.get_ques, name="get_qustions"),
    path('add-quiz/', views.add_quiz, name="add_quiz"),
    path('add-group-quiz/', views.add_group_quiz, name="add_group_quiz"),
    path('add-question/<title>/', views.add_question, name="add_question"),
    path('get-user-quiz/', views.get_user_quiz, name="get_user_quiz"),
    path('search/<str:item>/', views.search_user, name="search_user"),
    path('add-group/', views.add_group, name="add_group"),
    path('edit-profile/', views.edit_profile, name="edit_profile"),
    path('get-chats/<username>/', views.get_chats, name="get_chats"),
    #path('fetch-messages/<username>/', views.get_chats, name="get_chats"),
    path('send-chat/<username>/', views.send_chat, name="send_chat"),
]
