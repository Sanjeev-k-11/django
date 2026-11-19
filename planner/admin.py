from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import StudySession, Exam, TimetableEntry, Reminder


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'start', 'duration_display', 'notes_snippet', 'created_at')
    list_filter = ('start', 'subject', 'user')
    search_fields = ('user__username', 'notes', 'subject__name')

    @admin.display(description='Duration')
    def duration_display(self, obj):
        return format_html('<b>{} mins</b> ({} hrs)', obj.duration_minutes, obj.hours)

    @admin.display(description='Notes')
    def notes_snippet(self, obj):
        return obj.notes[:50] + "..." if len(obj.notes) > 50 else (obj.notes or "-")


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'user', 'date', 'countdown_badge', 'score_display', 'grade_badge', 'location')
    list_filter = ('date', 'subject', 'user')
    search_fields = ('title', 'location', 'syllabus_notes', 'user__username')

    @admin.display(description='Countdown')
    def countdown_badge(self, obj):
        return format_html('<span style="font-weight:bold; color:#7C3AED;">{}</span>', obj.countdown_text)

    @admin.display(description='Score')
    def score_display(self, obj):
        if obj.marks_obtained is not None and obj.total_marks:
            return f"{obj.marks_obtained} / {obj.total_marks} ({obj.percentage}%)"
        return "Pending"

    @admin.display(description='Grade')
    def grade_badge(self, obj):
        if obj.grade != "N/A":
            return format_html('<span style="padding:2px 8px; border-radius:10px; background:#F0FDF4; color:#16A34A; font-weight:bold;">{}</span>', obj.grade)
        return "—"


@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ('day_of_week_display', 'subject', 'user', 'time_slot', 'room')
    list_filter = ('day_of_week', 'subject', 'user')
    search_fields = ('subject__name', 'room', 'user__username')

    @admin.display(description='Day')
    def day_of_week_display(self, obj):
        return format_html('<strong>{}</strong>', obj.get_day_of_week_display())

    @admin.display(description='Time Slot')
    def time_slot(self, obj):
        return f"{obj.start_time.strftime('%H:%M')} – {obj.end_time.strftime('%H:%M')}"


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'datetime', 'status_badge')
    list_filter = ('is_done', 'datetime', 'user')
    search_fields = ('title', 'user__username')

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.is_done:
            return mark_safe('<span style="color:#16A34A; font-weight:bold;">✓ Completed</span>')
        return mark_safe('<span style="color:#F59E0B; font-weight:bold;">⏳ Active</span>')
