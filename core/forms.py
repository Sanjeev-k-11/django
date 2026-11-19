from django import forms
from .models import Subject, StudyGoal, Assignment, Note, ChecklistItem


class SubjectForm(forms.ModelForm):
    color = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-color-picker'}),
        initial='#2563EB',
        help_text="Choose a theme color for this subject"
    )

    class Meta:
        model = Subject
        fields = ['name', 'code', 'teacher', 'color', 'target_grade', 'is_archived']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Data Structures & Algorithms'}),
            'code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. CS201'}),
            'teacher': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Dr. Alan Turing'}),
            'target_grade': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. A+ or 90%'}),
            'is_archived': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['subject', 'title', 'description', 'due_date', 'due_time', 'priority', 'status', 'attachment']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Chapter 4 Problem Set'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Assignment requirements, guidelines, questions...'}),
            'due_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'attachment': forms.FileInput(attrs={'class': 'form-file-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user, is_archived=False)

    def clean_attachment(self):
        attachment = self.cleaned_data.get('attachment')
        if attachment and hasattr(attachment, 'size'):
            # 10MB limit
            if attachment.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File attachment size must not exceed 10MB.")
        return attachment


class StudyGoalForm(forms.ModelForm):
    class Meta:
        model = StudyGoal
        fields = ['subject', 'title', 'description', 'target_date', 'goal_type', 'status', 'progress']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Master Binary Search Trees'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Specific milestones or objectives...'}),
            'target_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'goal_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'progress': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'max': '100', 'step': '5'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['subject', 'title', 'content', 'tags', 'is_pinned']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Quick Formula Sheet - Physics'}),
            'content': forms.Textarea(attrs={'class': 'form-input note-content-area', 'rows': 12, 'placeholder': 'Write your comprehensive study notes here...'}),
            'tags': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. exam, formula, week3 (comma separated)'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)


class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input subtask-input', 'placeholder': 'Add a subtask or milestone...'}),
        }
