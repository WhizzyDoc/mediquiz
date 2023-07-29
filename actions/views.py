from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from.models import Action
from quiz.models import Profile, Group, Quiz, Score, Question, Chat
from .decorators import ajax_required
from .utils import create_action
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
import re
import json
from django.db.models import Q

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s

# Create your views here.
@login_required(login_url='login')
def activity(request):
    user = get_object_or_404(Profile, user=request.user)
    actions = Action.objects.exclude(user=user)[:10]
    activity = Action.objects.filter(user=user)[:10]
    #actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:20]
    return render(request, 'actions/activity.html', {
        'actions': actions,
        'activity': activity,
        'user': user,
    })

@login_required(login_url='login')
def search_user(request, item):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        users = User.objects.filter(Q(username__icontains=item))
        groups = Group.objects.filter(Q(title__icontains=item) | Q(description__icontains=item))
        quiz = Quiz.objects.filter(Q(title__icontains=item))
        return JsonResponse({
            "users":list(users.values()),
            "groups": list(groups.values()),
            "quiz": list(quiz.values())
        })

@login_required(login_url='login')
@csrf_exempt
def get_chats(request, username):
    user = request.user.username
    chats = Chat.objects.filter(Q(sender__iexact=user, receiver__iexact=username) |
                                Q(sender__iexact=username, receiver__iexact=user))
    for chat in chats:
        chat.seen = True
        chat.save()
    return JsonResponse({
        "chats": list(chats.values()),
        "user": user,
    })

@login_required(login_url='login')
def send_chat(request, username):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == "POST":
            user = request.user.username
            message = request.POST.get('message')
            new_message = Chat(sender=user, receiver=username, message=message)
            new_message.save()
            return JsonResponse({
                'status': 'ok',
            })



#@ajax_required
@require_POST
@login_required(login_url='login')
def join_group(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group_slug = json.load(request)['slug']
        action = ''
        if group_slug:
            try:
                group = get_object_or_404(Group, slug=group_slug)
                if request.user not in group.members.all():
                    group.members.add(request.user)
                    group.save()
                    create_action(profile, 'joined', group)
                    action = 'join'
                else:
                    group.members.remove(request.user)
                    if request.user in group.admins.all():
                        group.admins.remove(request.user)
                    group.save()
                    action = 'leave'
                return JsonResponse({'status':'ok', 'action':action})
            except Group.DoesNotExist:
                return JsonResponse({'status':'error'})
    return JsonResponse({'status': 'error'})

@require_POST
@login_required(login_url='login')
def delete_quiz(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        quiz_slug = json.load(request)['slug']
        if quiz_slug:
            try:
                quiz = get_object_or_404(Quiz, slug=quiz_slug)
                quiz.delete()
                return JsonResponse({'status':'ok', 'title': quiz.title})
            except Quiz.DoesNotExist:
                return JsonResponse({'status':'error'})
    return JsonResponse({'status': 'error'})

@login_required(login_url='login')
def group_quiz(request, slug):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group = get_object_or_404(Group, slug=slug)
        all_quiz = group.quizzes.all()
        return JsonResponse({
            "quiz":list(all_quiz.values())
        })

@require_POST
@login_required(login_url='login')
def submit_quiz(request, slug):
    profile = get_object_or_404(Profile, user=request.user)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        quiz = get_object_or_404(Quiz,slug=slug)
        questions = Question.objects.filter(quiz=quiz)
        mark = json.load(request)['score']
        remark = ''
        score = round((int(mark) / int(questions.count())) * 100, 1)
        if score >= 80:
            remark = "Gold"
        elif score < 80 and score >= 60:
            remark = "Silver"
        elif score < 60 and score >= 40:
            remark = "Bronze"
        elif score < 40:
            remark = "Copper"
        if Score.objects.filter(student=profile, quiz=quiz).exists():
            u_score = get_object_or_404(Score, student=profile, quiz=quiz)
            u_score.delete()
        Score.objects.create(student=profile, name=request.user.username, quiz=quiz, score=score, remark=remark)
        create_action(profile, 'participated in a quiz', quiz)
        return JsonResponse({
            'score': score,
            'remark': remark,
        })


@login_required(login_url='login')
def quiz_rank(request, slug):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        quiz = get_object_or_404(Quiz, slug=slug)
        scores = Score.objects.filter(quiz=quiz)
        return JsonResponse({
            "scores":list(scores.values())
        })

@login_required(login_url='login')
def get_ques(request, slug, order):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        quiz = get_object_or_404(Quiz, slug=slug)
        question = get_object_or_404(Question, quiz=quiz, order=order)
        if question.image:
            return JsonResponse({
                "question":question.question,
                'order': question.order,
                "option_a": question.optionA,
                "option_b": question.optionB,
                "option_c": question.optionC,
                "option_d": question.optionD,
                "answer": question.answer,
                "image": question.image.url,
            })
        else:
            return JsonResponse({
                "question": question.question,
                'order': question.order,
                "option_a": question.optionA,
                "option_b": question.optionB,
                "option_c": question.optionC,
                "option_d": question.optionD,
                "answer": question.answer,
            })


@require_POST
@login_required(login_url='login')
def add_quiz(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form_data = json.loads(request.body)
        title = form_data.get('title')
        t = slugify(title)
        duration = form_data.get('duration')
        if title and duration:
            new_quiz = Quiz(title=title, duration=duration, slug=t)
            new_quiz.save()
            profile.quiz.add(new_quiz)
            profile.save()
            create_action(profile, 'created a quiz', new_quiz)
            quiz = get_object_or_404(Quiz, slug=t)
            data = {
                'quiz': {
                    'title': quiz.title,
                    'slug': quiz.slug,
                    'duration': quiz.duration,
                    'active': quiz.active,
                    'questions': quiz.questions.count(),
                    'participants': quiz.score.count(),
                }
            }
            return JsonResponse(data)
    return JsonResponse({'status': 'error'})

@require_POST
@login_required(login_url='login')
def add_group_quiz(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group_title = request.POST.get('group-title')
        quiz_title = request.POST.get('quiz-title')
        duration = request.POST.get('duration')
        slug = slugify(quiz_title)
        group = get_object_or_404(Group, title=group_title)
        if group_title and quiz_title and duration:
            new_quiz = Quiz(title=quiz_title, duration=duration, slug=slug)
            new_quiz.save()
            profile.quiz.add(new_quiz)
            group.quizzes.add(new_quiz)
            profile.save()
            group.save()
            create_action(profile, f'created a quiz for {group.title}', new_quiz)
            quiz = get_object_or_404(Quiz, slug=slug)
            data = {
                'quiz': {
                    'title': quiz.title,
                    'slug': quiz.slug,
                    'duration': quiz.duration,
                    'active': quiz.active,
                    'questions': quiz.questions.count(),
                    'participants': quiz.score.count(),
                }
            }
            return JsonResponse(data)
    return JsonResponse({'status': 'error'})

@require_POST
@login_required(login_url='login')
def add_question(request, title):
    quiz = get_object_or_404(Quiz, title=title)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        order = request.POST.get('order')
        question = request.POST.get('question')
        optionA = request.POST.get('option_a')
        optionB = request.POST.get('option_b')
        optionC = request.POST.get('option_c')
        optionD = request.POST.get('option_d')
        answer = request.POST.get('answer')
        image = request.FILES.get('question-image')
        try:
            que = get_object_or_404(Question, quiz=quiz, order=order)
            return JsonResponse({'error': f'Question Number {order} Already Exists.'})
        except:
            new_question = Question(quiz=quiz, order=order, question=question, image=image, optionA=optionA,
                                    optionB=optionB, optionC=optionC, optionD=optionD, answer=answer)
            new_question.save()
            data = {'order': order}
            return JsonResponse(data)
    return JsonResponse({'status': 'error'})


@login_required(login_url='login')
def get_user_quiz(request):
    user = get_object_or_404(User, username=request.user.username)
    profile = get_object_or_404(Profile, user=user)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        quiz = profile.quiz.all()
        return JsonResponse({
            "quiz": list(quiz.values())
        })

@ajax_required
@require_POST
@login_required(login_url='login')
def add_group(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        title = request.POST.get('group-title')
        t = slugify(title)
        des = request.POST.get('group-description')
        type = request.POST.get('group-type')
        image = request.FILES.get('group-image')
    
        if title and des and type and image:
            new_group = Group(title=title, slug=t, description=des, type=type, image=image)
            new_group.save()
            new_group.members.add(request.user)
            new_group.admins.add(request.user)
            new_group.save()
            create_action(profile, 'created a group', new_group)
            group = get_object_or_404(Group, slug=t)
            data = {
                'group': {
                    'title': group.title,
                    'slug': group.slug,
                    'image': group.image.url,
                    'type': group.type,
                    'des': group.description,
                    'link': group.get_group_detail(),
                    'members': group.members.count(),
                    'quiz': group.quizzes.count(),
                }
            }
            return JsonResponse(data)
    return JsonResponse({'status': 'error'})

@ajax_required
@require_POST
@login_required(login_url='login')
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    fname = request.POST.get('first-name')
    lname = request.POST.get('last-name')
    about = request.POST.get('about')
    school = request.POST.get('school')
    course = request.POST.get('course')
    image = request.FILES.get('profile-image')
    profile.f_name = fname
    profile.l_name = lname
    profile.about = about
    profile.school = school
    profile.course = course
    if image:
        profile.photo = image
    profile.save()
    data = {
        'profile':{
            'fname': profile.f_name,
            'lname': profile.l_name,
            'about': profile.about,
            'school': profile.school,
            'course': profile.course,
        }
    }
    return JsonResponse(data)
