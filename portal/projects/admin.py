from django.contrib import admin
from .models import Subject, LectureNote, MainProject, MiniProject, ProjectFile, Semester

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(LectureNote)
class LectureNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'uploaded_by', 'date_uploaded')
    search_fields = ('title', 'description')

@admin.register(MainProject)
class MainProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'subject', 'student_list', 'year') 
    search_fields = ('title', 'description', 'subject')
    list_filter = ('year',) 
    def student_list(self, obj):
        # Display the students associated with the main project
        return ", ".join([student.username for student in obj.students.all()])
    student_list.short_description = 'Students'  # Custom label for the column

@admin.register(MiniProject)
class MiniProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'student_1', 'uploaded_by', 'date_created')
    search_fields = ('title', 'description', 'student_1', 'student_2', 'student_3', 'student_4')

@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('file_type', 'file', 'uploaded_at')
