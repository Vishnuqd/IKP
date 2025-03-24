from django.urls import path
from .views import register, user_login, user_logout
from .views import student_dashboard
from . import views
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('reject-user/<int:user_id>/', views.reject_user, name='reject_user'),
    
]

