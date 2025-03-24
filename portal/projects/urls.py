# projects/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', views.faculty_dashboard, name='faculty_dashboard'),

    # Lecture Notes
    path('upload-note/', views.upload_lecture_note, name='upload_lecture_note'),
    path('get_subjects/', views.get_subjects, name='get_subjects'),
    # Main Project
    path('main/create/', views.create_main_project, name='create_main_project'),
    path('main/', views.list_main_projects, name='list_main_projects'),
    path('notes/', views.list_lecture_notes, name='list_lecture_notes'),
    path('all-notes/', views.list_all_lecture_notes, name='list_all_lecture_notes'),
    path('main/<int:pk>/add-files/', views.add_files_to_main_project, name='add_files_to_main_project'),
    path('main/<int:pk>/edit/', views.create_main_project, name='edit_main_project'),
    path('main/<int:pk>/view/', views.view_main_project, name='view_main_project'),  
    # Mini Project
    path('mini/create/', views.create_mini_project, name='create_mini_project'),
    path('mini/', views.list_mini_projects, name='list_mini_projects'),
    path('mini/<int:pk>/add-files/', views.add_files_to_mini_project, name='add_files_to_mini_project'),
    path('upload/', views.upload_question_paper, name='upload_question_paper'),
    path('view/', views.view_question_papers, name='view_question_papers'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)