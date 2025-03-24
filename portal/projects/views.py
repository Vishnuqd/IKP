# projects/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.decorators import faculty_required
from django.http import JsonResponse

from .models import Assignment, AssignmentSubmission, LectureNote, MainProject, MiniProject, ProjectFile, Subject, Semester, QuestionBank
from users.models import CustomUser
from .forms import AssignmentForm, AssignmentSubmissionForm, LectureNoteForm, MainProjectForm, MiniProjectForm, ProjectFileForm, QuestionBankForm

@login_required
@faculty_required
def faculty_dashboard(request):
    if not request.user.is_approved:
        messages.error(request, "Your account is pending approval.", extra_tags="custom-error")
        return redirect('home')
    # For example, show counts of LectureNotes, MainProjects, Question Bank
    note_count = LectureNote.objects.filter(uploaded_by=request.user).count()
    main_count = MainProject.objects.filter().count()
    question_bank = QuestionBank.objects.filter().count()
    assignment_count = Assignment.objects.filter(created_by=request.user).count()

    context = {
        'note_count': note_count,
        'main_count': main_count,
        'question_bank': question_bank,
        'assignment_count': assignment_count,
    }
    return render(request, 'projects/faculty_dashboard.html', context)


@login_required
@faculty_required
def upload_lecture_note(request):
    semesters = Semester.objects.all()  # Fetch all semesters
    if request.method == 'POST':
        form = LectureNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            messages.success(request, "Lecture note uploaded successfully!")
            return redirect('faculty_dashboard')
        else:
            print("Form Errors:", form.errors)
            messages.error(request, "Error in form submission. Please check your inputs.")
    else:
        form = LectureNoteForm()
    return render(request, 'projects/upload_lecture_note.html', {'form': form, 'semesters': semesters})


@login_required
@faculty_required
def list_lecture_notes(request):
    notes = LectureNote.objects.filter(uploaded_by=request.user)
    return render(request, 'projects/list_lecture_notes.html', {'lecture_notes': notes})

@login_required
def list_all_lecture_notes(request):
    notes = LectureNote.objects.all()
    return render(request, 'projects/list_all_lecture_notes.html', {'lecture_notes': notes})

@login_required
@faculty_required
def create_main_project(request, pk=None):
    # If pk is provided, we're editing an existing project
    if pk:
        project = get_object_or_404(MainProject, pk=pk, uploaded_by=request.user)
    else:
        project = None  # No pk means we're creating a new project

    students = CustomUser.objects.filter(role='student')  # Fetch all users with the role 'student'
    
    if request.method == 'POST':
        form = MainProjectForm(request.POST, instance=project)  # Pass the project instance if editing
        if form.is_valid():
            main_project = form.save(commit=False)
            main_project.uploaded_by = request.user  # Ensure the current user is set as the uploader
            main_project.save()

            # Add the selected students to the project dynamically
            students_selected = form.cleaned_data['students']
            main_project.students.set(students_selected)  # Add or remove students dynamically
            main_project.save()

            # Set the year field (it should already be handled by the form)
            main_project.year = form.cleaned_data['year']
            main_project.save()

            if project:
                messages.success(request, "Main project updated successfully!")
            else:
                messages.success(request, "Main project created successfully!")
            return redirect('list_main_projects')
    else:
        form = MainProjectForm(instance=project)  # Use the form with the existing project data if editing

    return render(request, 'projects/create_main_project.html', {'form': form, 'students': students, 'project': project})

@login_required
@faculty_required
def edit_main_project(request, pk):
    project = get_object_or_404(MainProject, pk=pk, uploaded_by=request.user)

    if request.method == 'POST':
        form = MainProjectForm(request.POST, instance=project)
        if form.is_valid():
            updated_project = form.save(commit=False)
            updated_project.uploaded_by = request.user
            updated_project.save()

            # Update students if changed
            students_selected = form.cleaned_data['students']
            updated_project.students.set(students_selected)  # Add/Remove students
            updated_project.save()

            messages.success(request, "Main project updated successfully!")
            return redirect('list_main_projects')
    else:
        form = MainProjectForm(instance=project)

    return render(request, 'projects/edit_main_project.html', {'form': form, 'project': project})

@login_required

def view_main_project(request, pk):
    project = get_object_or_404(MainProject, pk=pk)

    # Fetch all files related to the project (both main and mini project files)
    project_files = ProjectFile.objects.filter(main_project=project)

    return render(request, 'projects/view_main_project.html', {'project': project, 'project_files': project_files})

@login_required

def list_main_projects(request):
    # Get the filter criteria from GET params (year and branch)
    year = request.GET.get('year', '')
    branch = request.GET.get('branch', '')

    # Get all projects
    projects = MainProject.objects.all()

    # Filter by year and branch if provided
    if year:
        projects = projects.filter(year=year)

    if branch:
        projects = projects.filter(branch=branch)

    # Process each project to see if the current user is part of it
    projects_with_access = []
    for project in projects:
        is_part_of_project = project.students.filter(id=request.user.id).exists()  # Check if user is part of the project
        projects_with_access.append({'project': project, 'is_part_of_project': is_part_of_project})

    return render(request, 'projects/list_main_projects.html', {
        'projects_with_access': projects_with_access,
        'year': year,
        'branch': branch
    })

@login_required

def add_files_to_main_project(request, pk):
    main_project = get_object_or_404(MainProject, pk=pk)
    
    if request.user.role == 'student':
    # Check if the student is part of the project
        if request.user not in main_project.students.all():
            messages.error(request, "You are not authorized to add files to this project.")
            return redirect('student_dashboard')  # Redirect them to the dashboard or appropriate page

    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES)
        if form.is_valid():
            project_file = form.save(commit=False)
            project_file.main_project = main_project
            project_file.uploaded_by = request.user
            project_file.save()
            messages.success(request, "File added successfully!")
            return redirect('view_main_project', pk=main_project.pk)
    else:
        form = ProjectFileForm()

    return render(request, 'projects/add_files_to_main_project.html', {'form': form, 'project': main_project})

def upload_question_paper(request):
    if request.method == 'POST':
        form = QuestionBankForm(request.POST, request.FILES)
        if form.is_valid():
            print(f"Selected subject ID: {form.cleaned_data['subject'].id}")  # Debugging: print selected subject ID
            question_paper = form.save(commit=False)
            question_paper.uploaded_by = request.user  # ✅ Set uploader
            question_paper.save()
            messages.success(request, "Question paper uploaded successfully!")
            return redirect('view_question_papers')  # Redirect to the page showing uploaded question papers
        else:
            # Print form errors for debugging
            print("Form errors:", form.errors)  # Debugging: print the errors
            messages.error(request, "Error uploading the question paper. check your input.")
    else:
        form = QuestionBankForm()
    
    return render(request, 'projects/upload_question_paper.html', {'form': form})

def view_question_papers(request):
    question_papers = QuestionBank.objects.all()
    return render(request, 'projects/view_question_papers.html', {'question_papers': question_papers})


@login_required
@faculty_required
def create_mini_project(request):
    if request.method == 'POST':
        form = MiniProjectForm(request.POST)
        if form.is_valid():
            mini_project = form.save(commit=False)
            mini_project.uploaded_by = request.user
            mini_project.save()
            return redirect('list_mini_projects')
    else:
        form = MiniProjectForm()
    return render(request, 'projects/create_mini_project.html', {'form': form})


@login_required
@faculty_required
def list_mini_projects(request):
    projects = MiniProject.objects.filter(uploaded_by=request.user)
    return render(request, 'projects/list_mini_projects.html', {'projects': projects})


@login_required
@faculty_required
def add_files_to_mini_project(request, pk):
    mini_project = get_object_or_404(MiniProject, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES)
        if form.is_valid():
            project_file = form.save(commit=False)
            project_file.mini_project = mini_project
            project_file.save()
            return redirect('list_mini_projects')  # or detail view
    else:
        form = ProjectFileForm()
    context = {
        'project': mini_project,
        'form': form,
    }
    return render(request, 'projects/add_files_to_mini_project.html', context)

def get_subjects(request):
    semester_id = request.GET.get('semester_id')  # Get the selected semester id
    subjects = Subject.objects.filter(semester_id=semester_id)  # Filter subjects based on semester
    subject_data = list(subjects.values('id', 'name'))  # Get subject id and name
    print("Fetched subjects:", subject_data) 
    return JsonResponse({'subjects': subject_data})

@login_required
@faculty_required
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.created_by = request.user
            assignment.save()
            messages.success(request, "Assignment created successfully!")
            return redirect('faculty_list_assignments')
    else:
        form = AssignmentForm()
    return render(request, 'projects/create_assignment.html', {'form': form})


@login_required
@faculty_required
def faculty_list_assignments(request):
    assignments = Assignment.objects.filter(created_by=request.user).order_by('-date_created')
    return render(request, 'projects/faculty_list_assignments.html', {'assignments': assignments})


@login_required
@faculty_required
def view_assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, created_by=request.user)
    submissions = AssignmentSubmission.objects.filter(assignment=assignment)
    return render(request, 'projects/view_assignment_detail.html', {
        'assignment': assignment,
        'submissions': submissions
    })

@login_required
def list_assignments(request):
    semester_id = request.GET.get('semester')
    subject_id = request.GET.get('subject')

    assignments = Assignment.objects.all().order_by('-date_created')
    if semester_id:
        assignments = assignments.filter(semester_id=semester_id)
    if subject_id:
        assignments = assignments.filter(subject_id=subject_id)

    semesters = Semester.objects.all()
    subjects = Subject.objects.all()

    # To check if the current user has already submitted each
    assignment_info = []
    for a in assignments:
        submitted = AssignmentSubmission.objects.filter(assignment=a, student=request.user).first()
        assignment_info.append({
            'assignment': a,
            'submission': submitted,
        })

    return render(request, 'projects/list_assignments.html', {
        'assignment_info': assignment_info,
        'semesters': semesters,
        'subjects': subjects,
        'selected_semester': semester_id,
        'selected_subject': subject_id,
    })

@login_required
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    # Prevent multiple submissions
    if AssignmentSubmission.objects.filter(assignment=assignment, student=request.user).exists():
        messages.info(request, "You have already submitted this assignment.")
        return redirect('list_assignments')

    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, "Assignment submitted successfully!")
            return redirect('list_assignments')
    else:
        form = AssignmentSubmissionForm()

    return render(request, 'projects/submit_assignment.html', {'form': form, 'assignment': assignment})