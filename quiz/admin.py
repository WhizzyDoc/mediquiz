from django.contrib import admin
from .models import Profile, Group, Quiz, Question, Score, Chat, Developer

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'f_name', 'l_name']
    
@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'organization', 'skill', 'location', 'email']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'description']
    list_filter = ['type']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['type',]
    list_per_page = 20

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'duration', 'active', 'created']
    list_filter = ['active']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['active',]
    list_per_page = 20

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'order', 'question']
    list_filter = ['quiz']
    list_per_page = 20

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['student', 'name', 'quiz', 'score', 'remark', 'created']
    list_filter = ['quiz', 'remark']
    list_editable = ['remark',]
    list_per_page = 20

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message', 'seen', 'date']
    list_filter = ['sender', 'receiver', 'seen']
    list_per_page = 20
