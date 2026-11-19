from django import forms
from .models import StudySession, Exam, TimetableEntry, Reminder
from core.models import Subject


class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['subject', 'start', 'duration_minutes', 'notes']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'start': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-input', 'min': '1', 'max': '720'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'What topics did you review or practice?'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['subject', 'title', 'date', 'time', 'location', 'syllabus_notes', 'marks_obtained', 'total_marks']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Midterm Examination'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Science Auditorium / Online'}),
            'syllabus_notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Chapters 1-5, Calculator allowed...'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.5', 'placeholder': 'Optional marks'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.5', 'placeholder': 'e.g. 100'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)


class TimetableEntryForm(forms.ModelForm):
    class Meta:
        model = TimetableEntry
        fields = ['subject', 'day_of_week', 'start_time', 'end_time', 'room']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'day_of_week': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'room': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Hall 101, Lab B'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end and start >= end:
            self.add_error('end_time', "End time must be after start time.")
        return cleaned_data


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'datetime', 'is_done']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Return Library Books'}),
            'datetime': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
