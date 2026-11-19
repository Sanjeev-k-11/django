from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime, timedelta


class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=30, blank=True, help_text="e.g. CS101 or MATH201")
    teacher = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=20, default='#2563EB', help_text="Hex color code, e.g. #2563EB")
    target_grade = models.CharField(max_length=20, blank=True, help_text="e.g. A+, 95%")
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.code} - {self.name}" if self.code else self.name

    @property
    def total_assignments(self):
        return self.assignments.count()

    @property
    def completed_assignments(self):
        return self.assignments.filter(status='completed').count()

    @property
    def assignment_progress(self):
        total = self.total_assignments
        if total == 0:
            return 0
        return int((self.completed_assignments / total) * 100)

    @property
    def total_study_minutes(self):
        total = self.study_sessions.aggregate(total=models.Sum('duration_minutes'))['total']
        return total or 0

    @property
    def total_study_hours(self):
        return round(self.total_study_minutes / 60.0, 1)


class StudyGoal(models.Model):
    GOAL_TYPES = (
        ('daily', 'Daily Goal'),
        ('weekly', 'Weekly Goal'),
        ('long_term', 'Long-term Goal'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_goals')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_date = models.DateField()
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES, default='weekly')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress = models.PositiveSmallIntegerField(default=0, help_text="Progress from 0 to 100%")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['target_date', '-created_at']

    def __str__(self):
        return self.title

    @property
    def days_left(self):
        today = date.today()
        diff = (self.target_date - today).days
        return diff


class Assignment(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    due_time = models.TimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    completed_at = models.DateTimeField(null=True, blank=True)
    attachment = models.FileField(upload_to='assignments/%Y/%m/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', 'due_time', '-priority']

    def __str__(self):
        return f"{self.title} ({self.subject.name})"

    @property
    def is_completed(self):
        return self.status == 'completed'

    @property
    def is_overdue(self):
        if self.is_completed:
            return False
        return self.due_date < date.today()

    @property
    def is_due_soon(self):
        """Due today, tomorrow, or in 2 days and not completed."""
        if self.is_completed:
            return False
        today = date.today()
        days_left = (self.due_date - today).days
        return 0 <= days_left <= 2

    @property
    def countdown_text(self):
        if self.is_completed:
            return "Completed"
        today = date.today()
        delta = (self.due_date - today).days
        if delta < 0:
            abs_days = abs(delta)
            return f"Overdue by {abs_days} day{'s' if abs_days != 1 else ''}"
        elif delta == 0:
            return "Due today"
        elif delta == 1:
            return "Due tomorrow"
        else:
            return f"Due in {delta} days"

    @property
    def subtasks_count(self):
        return self.subtasks.count()

    @property
    def subtasks_done_count(self):
        return self.subtasks.filter(is_done=True).count()

    @property
    def subtasks_progress_percent(self):
        total = self.subtasks_count
        if total == 0:
            return 100 if self.is_completed else 0
        return int((self.subtasks_done_count / total) * 100)


class ChecklistItem(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks')
    goal = models.ForeignKey(StudyGoal, on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks')
    title = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.CharField(max_length=250, blank=True, help_text="Comma-separated tags (e.g. formulas, exam-prep, summary)")
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]
