from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from quiz.models import Profile, Group, Question, Quiz, Chat, Score, Developer
from .forms import ProfileForm


# Create your views here.
@csrf_protect
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin_dashboard')
                else:
                    messages.warning(request, 'Sorry, you do not have permission to login as an Admin!')
                    return redirect('admin_login')
            else:
                messages.warning(request, 'Your account has been disabled!')
                return redirect('admin_login')
        else:
            messages.warning(request, 'Invalid Login!')
            return redirect('admin_login')
    return render(request, 'owner/admin-login.html')

@login_required(login_url='admin_login')
def dashboard(request):
    me = get_object_or_404(User, username=request.user.username)
    return render(request, 'owner/index.html', {
        'me': me,
    })


"""
Users
"""
@login_required(login_url='admin_login')
def user_list(request):
    query = request.GET.get('q')
    if query:
        object_list = Profile.objects.filter(Q(f_name__icontains=query) | Q(l_name__icontains=query) |
                                             Q(about__icontains=query) | Q(course__icontains=query))
    else:
        object_list = Profile.objects.all()
    user_count = object_list.count
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'owner/users/user-list.html', {
        'users': users,
        'page': page,
        'query': query,
        'count': user_count,
    })

def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    dp = "/static/image/avatar.png"
    if profile.photo:
        dp = str(profile.photo.url)
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
            }
        }
        return JsonResponse(data)

@login_required(login_url='admin_login')
@csrf_protect
def account_status(request, username):
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        if user.is_active:
            user.is_active = False
            user.save()
            messages.success(request, 'Account deactivated successfully!')
            return redirect('user_list')
        else:
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully!')
            return redirect('user_list')

@login_required(login_url='admin_login')
def user_edit(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        edit_form = ProfileForm(instance=profile, data=request.POST, files=request.FILES)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, f'{username}\'s account updated succesfully!')
            return redirect('user_list')
        else:
            messages.warning(request, 'Error updating profile!')
    else:
        edit_form = ProfileForm(instance=profile)
    return render(request, 'owner/users/user-edit.html', {
        'edit_form':  edit_form,
        'profile': profile,
        'user': user,
    })

@login_required(login_url='admin_login')
@csrf_protect
def user_delete(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('user_list')
    return render(request, 'owner/users/user-delete.html', {
        'user': user,
        'profile': profile,
    })


"""
Groups
"""
@login_required(login_url='admin_login')
def group_list(request):
    query = request.GET.get('q')
    if query:
        object_list = Group.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) |
                                             Q(type__icontains=query))
    else:
        object_list = Group.objects.all()
    group_count = object_list.count
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)
    return render(request, 'owner/group/group-list.html', {
        'groups': groups,
        'page': page,
        'query': query,
        'count': group_count,
    })

"""
Messages

@login_required(login_url='admin_login')
def message_add(request):
    if request.method == 'POST':
        add_form = FrameForm(data=request.POST)
        if add_form.is_valid():
            add_form.save()
            messages.success(request, 'New framework added successfully!')
            return redirect('frame_list')
        else:
            messages.warning(request, 'Error adding framework')
    else:
        add_form = FrameForm()
    return render(request, 'owner/message/message-add.html', {
        'add_form': add_form,
    })

@login_required(login_url='admin_login')
def message_edit(request, id):
    msg = get_object_or_404(Contact, id=id)
    sent = False
    if request.method == 'POST':
        edit_form = ContactForm(instance=msg, data=request.POST)
        if edit_form.is_valid():
            form = edit_form.save(commit=False)
            if form.reply:
                subject = f"{form.message}"
                message = f"Hi, {form.name}\n\n{form.reply}"
                send_mail(subject, message, 'rigantech@gmail.com', [form.email])
                sent = True
                form.save()
                messages.success(request, f'Reply sent to {form.email} as e-mail succesfully!')
                return redirect('message_list')
            messages.success(request, f'Message has not been replied to yet!')
            return redirect('message_list')
        else:
            messages.warning(request, 'Error updating framework!')
    else:
        edit_form = ContactForm(instance=msg)
    return render(request, 'owner/message/message-edit.html', {
        'edit_form':  edit_form,
        'msg': msg,
        'sent': sent,
    })



"""
