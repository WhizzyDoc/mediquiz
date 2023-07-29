from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
#Quiz Model
class Quiz(models.Model):
    title = models.CharField(max_length=100, verbose_name="Quiz Title")
    slug = models.SlugField(max_length=200, unique=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    date = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(verbose_name="Quiz Duration (mins)", null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_group_detail(self):
        return reverse('quiz_detail', args=[self.slug])
    
#Question Model
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions", verbose_name="Quiz", null=True)
    order = models.PositiveIntegerField(verbose_name="Question Order", default=1)
    question = models.TextField(null=True, blank=True, verbose_name="Question")
    image = models.ImageField(upload_to='questions/image/', blank=True, null=True, verbose_name='Question image')
    optionA = models.CharField(max_length=200, null=True, blank=True, verbose_name="Option A")
    optionB = models.CharField(max_length=200, null=True, blank=True, verbose_name="Option B")
    optionC = models.CharField(max_length=200, null=True, blank=True, verbose_name="Option C")
    optionD = models.CharField(max_length=200, null=True, blank=True, verbose_name="Option D")
    cat = (('optionA', 'optionA'), ('optionB', 'optionB'), ('optionC', 'optionC'), ('optionD', 'optionD'))
    answer = models.CharField(max_length=200, choices=cat)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'Question {self.order}'

# Groups Model
GROUP_CHOICES = (
    ('Public', 'Public'),
    ('Private', 'Private')
)
class Group(models.Model):
    title = models.CharField(max_length=100, verbose_name="Group Title", null=True)
    description = models.TextField(verbose_name="Group Description", null=True, blank=True)
    type = models.CharField(max_length=100, choices=GROUP_CHOICES, verbose_name="Group Type", default='Public')
    slug = models.SlugField(max_length=200, unique=True, null=True)
    image = models.ImageField(upload_to='groups/image/', blank=True, null=True, verbose_name='Group image')
    admins = models.ManyToManyField(User, related_name="group_admin", blank=True)
    members = models.ManyToManyField(User, related_name="group_member",blank=True)
    quizzes = models.ManyToManyField(Quiz, related_name="group", blank=True)

    def get_group_detail(self):
        return reverse('group_detail', args=[self.slug])

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

#Profile Model
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    f_name = models.CharField(max_length=100, verbose_name="First Name", null=True)
    l_name = models.CharField(max_length=100, verbose_name="Last Name", null=True)
    photo = models.ImageField(upload_to='users/photo/', blank=True, null=True, verbose_name='Profile Pic')
    about = models.TextField(verbose_name="About", null=True, blank=True)
    school = models.CharField(max_length=200, verbose_name="Institution", null=True, blank=True)
    course = models.CharField(max_length=200, verbose_name="Course Studying", null=True, blank=True)
    quiz = models.ManyToManyField(Quiz, related_name="creator", blank=True)

    def get_user_profile(self):
        return reverse('user_profile', args=[self.user.username])

    def __str__(self):
        return f'{self.f_name} {self.l_name}'

    class Meta:
        ordering = ['l_name']

# Score Model
REMARK_CHOICES = (
    ('Gold', 'Gold'),
    ('Silver', 'Silver'),
    ('Bronze', 'Bronze'),
    ('Copper', 'Copper'),
)
class Score(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="scores")
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="name")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="score")
    score = models.FloatField(verbose_name="Total Score")
    remark = models.CharField(max_length=100, choices=REMARK_CHOICES, null=True, blank=True, verbose_name="Remark")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student}'

    class Meta:
        ordering = ['-score']


class Chat(models.Model):
    sender = models.CharField(max_length=100, null=True, verbose_name="sender")
    receiver = models.CharField(max_length=100, null=True, verbose_name="receiver")
    message = models.TextField(verbose_name="message")
    date = models.DateTimeField(auto_now_add=True, null=True)
    seen = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f'{self.sender}'

    class Meta:
        ordering = ['date']

class Developer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="developer", null=True)
    nickname = models.CharField(max_length=100, verbose_name="Nickname", null=True)
    f_name = models.CharField(max_length=100, verbose_name="First Name", null=True)
    l_name = models.CharField(max_length=100, verbose_name="Last Name", null=True)
    photo = models.ImageField(upload_to='devs/photo/', blank=True, null=True, verbose_name='Profile Pic')
    about = models.TextField(verbose_name="About", null=True, blank=True)
    organization = models.CharField(max_length=200, verbose_name="Organization", null=True, blank=True)
    location = models.CharField(max_length=200, verbose_name="Location", null=True, blank=True)
    skill = models.CharField(max_length=200, verbose_name="Skills", null=True, blank=True)
    email = models.EmailField(max_length=200, verbose_name="Email", null=True, blank=True)
    phone_no = models.CharField(max_length=200, verbose_name="Phone Number", null=True, blank=True)
    website = models.URLField(max_length=200, verbose_name="website", null=True, blank=True)
    facebook = models.URLField(max_length=200, verbose_name="facebook", null=True, blank=True)
    twitter = models.URLField(max_length=200, verbose_name="twitter", null=True, blank=True)
    github = models.URLField(max_length=200, verbose_name="github", null=True, blank=True)
    whatsapp = models.URLField(max_length=200, verbose_name="whatsapp", null=True, blank=True)

    def __str__(self):
        return f'{self.nickname}'
