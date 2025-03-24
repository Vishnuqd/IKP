# projects/models.py

import os
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify 

class Semester(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects',default=1)
    
    def __str__(self):
       return f"{self.name} ({self.semester.name})"


class LectureNote(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    file = models.FileField(
        upload_to='uploads/lecture_notes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf','doc','docx','ppt','pptx','png'])]
    )
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MainProject(models.Model):
    BRANCH_CHOICES = (
        ('mechanical', 'Mechanical Engineering'),
        ('computer_science', 'Computer Science Engineering'),
        ('civil', 'Civil Engineering'),
        ('electronics', 'Electronics Engineering'),
        ('electrical', 'Electrical Engineering'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES, default='computer_science')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to={'role': 'student'}, blank=True, related_name='main_projects')  # Unique related_name
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    year = models.PositiveIntegerField(default=2025)

    def __str__(self):
        return f"{self.title} ({self.year})"


class MiniProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    student_1 = models.CharField(max_length=100)
    student_2 = models.CharField(max_length=100, blank=True, null=True)
    student_3 = models.CharField(max_length=100, blank=True, null=True)
    student_4 = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Mini Project)"

class QuestionBank(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_year = models.PositiveIntegerField()
    file = models.FileField(upload_to='uploads/questionbank/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Question Paper for {self.subject.name} ({self.exam_year})"

class ProjectFile(models.Model):
    FILE_TYPES = (
        ('SRS', 'SRS Document'),
        ('CODE', 'Codebase'),
        ('DOC', 'Documentation'),
        ('PPT', 'Presentation'),
        ('OTHER', 'Other'),
    )

    main_project = models.ForeignKey(MainProject, on_delete=models.CASCADE, null=True, blank=True, related_name='files')
    mini_project = models.ForeignKey(MiniProject, on_delete=models.CASCADE, null=True, blank=True, related_name='files')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='OTHER')
    file = models.FileField(upload_to='')  # Initially empty, will be handled by get_upload_to
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.main_project:
            return f"{self.file_type} for {self.main_project.title}"
        elif self.mini_project:
            return f"{self.file_type} for {self.mini_project.title}"
        return "Unassigned Project File"

    @staticmethod
    def get_upload_to(instance, filename):
        """Generate the path for file upload dynamically based on project title."""
        if instance.main_project:
            # Use the title of the project to create the folder, making sure to slugify it to avoid spaces and special chars.
            project_folder = slugify(instance.main_project.title)  # Slugify the project title for safe folder names
            return os.path.join('uploads/project_files', project_folder, filename)  # Custom folder for each project
        else:
            # If no main_project, use a default folder for mini_project or others
            return os.path.join('uploads/project_files', 'default', filename)

# Connect the method to the FileField
ProjectFile._meta.get_field('file').upload_to = ProjectFile.get_upload_to