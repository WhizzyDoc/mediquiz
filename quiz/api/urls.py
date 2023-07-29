from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'courses'
router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)

urlpatterns = [
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/<pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    # path('courses/<pk>/enroll/', views.CourseEnrollView.as_view(), name='course_enroll'),
    path('', include(router.urls)),
]
