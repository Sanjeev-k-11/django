from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime, timedelta


class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    subject = models.ForeignKey('core.Subject', on_delete=models.SET_NULL, null=True, blank=True, related_name='study_sessions')
    start = models.DateTimeField(default=timezone.now)
    duration_minutes = models.PositiveIntegerField(default=25, help_text="Duration in minutes")
    notes = models.TextField(blank=True, help_text="What did you study during this session?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start']

    def __str__(self):
        sub_name = self.subject.name if self.subject else "General Study"
        return f"{self.user.username} - {sub_name} ({self.duration_minutes}m)"

    @property
    def hours(self):
        return round(self.duration_minutes / 60.0, 2)


class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey('core.Subject', on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=150, blank=True, help_text="e.g. Hall B, Online, Room 402")
    syllabus_notes = models.TextField(blank=True, help_text="Topics covered, allowed materials, etc.")
    marks_obtained = models.FloatField(null=True, blank=True)
    total_marks = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.title} - {self.subject.name}"

    @property
    def is_past(self):
        return self.date < date.today()

    @property
    def days_left(self):
        return (self.date - date.today()).days

    @property
    def countdown_text(self):
        delta = self.days_left
        if delta < 0:
            return f"Completed ({abs(delta)} days ago)" if self.marks_obtained is not None else f"Passed {abs(delta)} days ago"
        elif delta == 0:
            return "Exam Today!"
        elif delta == 1:
            return "Exam Tomorrow!"
        else:
            return f"{delta} days left"

    @property
    def percentage(self):
        if self.marks_obtained is not None and self.total_marks and self.total_marks > 0:
            return round((self.marks_obtained / self.total_marks) * 100, 1)
        return None

    @property
    def grade(self):
        pct = self.percentage
        if pct is None:
            return "N/A"
        if pct >= 90:
            return "A+"
        elif pct >= 80:
            return "A"
        elif pct >= 70:
            return "B"
        elif pct >= 60:
            return "C"
        elif pct >= 50:
            return "D"
        else:
            return "F"


class TimetableEntry(models.Model):
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timetable_entries')
    subject = models.ForeignKey('core.Subject', on_delete=models.CASCADE, related_name='timetable_entries')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100, blank=True, help_text="e.g. Lab 3, Lecture Hall A")

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.subject.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['datetime']

    def __str__(self):
        return self.title
