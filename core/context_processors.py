from datetime import date, timedelta
from django.utils import timezone


def global_context(request):
    if not request.user.is_authenticated:
        return {}

    today = date.today()
    tomorrow = today + timedelta(days=1)
    two_days = today + timedelta(days=2)

    # Overdue assignments
    overdue_assignments = request.user.assignments.filter(
        due_date__lt=today
    ).exclude(status='completed').select_related('subject')

    # Due today & tomorrow assignments
    due_soon_assignments = request.user.assignments.filter(
        due_date__gte=today,
        due_date__lte=two_days
    ).exclude(status='completed').select_related('subject')

    # Upcoming exams in next 7 days
    next_week = today + timedelta(days=7)
    upcoming_exams = request.user.exams.filter(
        date__gte=today,
        date__lte=next_week
    ).select_related('subject')

    # Active reminders
    active_reminders = request.user.reminders.filter(
        is_done=False
    ).order_by('datetime')[:5]

    total_notifications = overdue_assignments.count() + due_soon_assignments.count() + upcoming_exams.count()

    return {
        'nav_overdue_assignments': overdue_assignments,
        'nav_due_soon_assignments': due_soon_assignments,
        'nav_upcoming_exams': upcoming_exams,
        'nav_active_reminders': active_reminders,
        'nav_notification_count': total_notifications,
        'current_today': today,
    }
