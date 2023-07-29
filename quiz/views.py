from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .forms import RegistrationForm, LoginForm, QuestionForm
from .models import Profile, Group, Quiz, Question, Score, Chat, Developer
from actions.utils import create_action
import datetime

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # create the user profile
            profile = Profile(user=new_user)
            profile.save()
            create_action(profile, 'created an account')
            messages.success(request, "Your account has been successfully created, kindly enter your login details below")
            return redirect('login')
    else:
        user_form = RegistrationForm()
    return render(request, 'registration/register.html', {
        'user_form': user_form
    })

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'WELCOME {user.username}!')
                    return redirect('dashboard')
                else:
                    messages.warning(request, 'Your account has been disabled!')
                    return redirect('login')
            else:
                messages.warning(request, 'Invalid Login!')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {
        'form': form
    })

def logout_view(request):
    logout(request)
    messages.warning(request, "You have been logged out, enter your details to log back in")
    return redirect('login')

def index(request):
    year = datetime.datetime.today().year
    developers = Developer.objects.all()
    return render(request, "quiz/index.html", {
        'year': year,
        'developers': developers,
        })

def privacy(request):
    return render(request, "quiz/privacy.html")

@login_required(login_url="login")
def dashboard(request):
    groups = Group.objects.filter(members__in=[request.user])
    student = get_object_or_404(Profile, user=request.user)
    quiz = student.quiz.all()
    return render(request, "user/dashboard.html", {
        'groups': groups,
        'student': student,
        'quiz': quiz,
    })

@login_required(login_url="login")
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'user/group_list.html', {
        'groups': groups,
    })

@login_required(login_url="login")
def group_detail(request, slug):
    group = get_object_or_404(Group, slug=slug)
    members = []
    admins = []
    users = User.objects.filter(is_active=True)
    for user in users:
        if user in group.members.all():
            member = get_object_or_404(Profile, user=user)
            members.append(member)
        else:
            pass
        if user in group.admins.all():
            admin = get_object_or_404(Profile, user=user)
            admins.append(admin)
        else:
            pass
    return render(request, 'user/group_detail.html', {
        'group': group,
        'members': members,
        'admins': admins,
    })

@login_required(login_url="login")
def quiz_list(request):
    quiz = Quiz.objects.filter(active=True)
    return render(request, 'user/quiz_list.html', {
        'quiz': quiz
    })

@login_required(login_url="login")
@csrf_exempt
def quiz_detail(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug)
    questions = Question.objects.filter(quiz=quiz)
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'quiz/quiz1.html', {
        'quiz': quiz,
        'questions': questions,
        'profile': profile,
    })

@login_required(login_url="login")
def people(request):
    user = get_object_or_404(Profile, user=request.user)
    users = Profile.objects.all().exclude(user=request.user)
    return render(request, 'user/people.html', {
        'users': users,
        'user': user,
    })

@login_required(login_url="login")
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    groups = Group.objects.filter(members__in=[user])
    quiz = profile.quiz.all()
    scores = profile.scores.all()
    s_quiz = []
    g_image = []
    dp = "/static/image/avatar.png"
    if profile.photo:
        dp = profile.photo.url
    if scores:
        for score in scores:
            s_quiz.append(score.quiz.title)
    if groups:
        for group in groups:
            g_image.append(group.image.url)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'profile': {
                'fname': profile.f_name,
                'lname': profile.l_name,
                'about': profile.about,
                'school': profile.school,
                'course': profile.course,
                'username': user.username,
                'dp': dp,
            },
            "quiz": list(quiz.values()),
            "groups": list(groups.values()),
            "scores": list(scores.values()),
            's_quiz': s_quiz,
            "g_image": g_image,
        }
        return JsonResponse(data)
    else:
        return render(request, 'user/user_profile.html', {
            'profile': profile,
            'groups': groups,
            'quiz': quiz,
            'user': user,
        })
