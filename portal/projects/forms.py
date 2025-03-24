# projects/forms.py

from django import forms
from .models import LectureNote, MainProject, MiniProject, ProjectFile, Semester, QuestionBank, Subject
from users.models import CustomUser

class LectureNoteForm(forms.ModelForm):
    class Meta:
        model = LectureNote
        fields = ['title', 'description','semester', 'subject', 'file']

    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
class MainProjectForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='student'),  # Only allow students to be selected
        widget=forms.CheckboxSelectMultiple,  # Multiple selection via checkboxes
        required=False  # Make it optional; you can adjust based on your needs
    )

    class Meta:
        model = MainProject
        fields = ['title', 'description', 'branch', 'students', 'year']

class MiniProjectForm(forms.ModelForm):
    class Meta:
        model = MiniProject
        fields = ['title', 'description', 'subject',
                  'student_1', 'student_2', 'student_3', 'student_4']

class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = ['file_type', 'file']

class QuestionBankForm(forms.ModelForm):
    class Meta:
        model = QuestionBank
        fields = ['name', 'description', 'semester', 'subject', 'exam_year', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Step 1: default to no subjects
        self.fields['subject'].queryset = Subject.objects.none()

        # Step 2: handle POST (when semester was selected)
        if 'semester' in self.data:
            try:
                semester_id = int(self.data.get('semester'))
                self.fields['subject'].queryset = Subject.objects.filter(semester_id=semester_id)
            except (ValueError, TypeError):
                pass  # invalid input, fallback to none
        # Step 3: if editing an instance (already saved with semester)
        elif self.instance.pk and self.instance.semester:
            self.fields['subject'].queryset = Subject.objects.filter(semester=self.instance.semester)

        # Add form-control classes
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise forms.ValidationError("This field is required.")
        if file.size > 10485760:  # Example: 10MB size limit
            raise forms.ValidationError("File size should not exceed 10MB.")
        return file