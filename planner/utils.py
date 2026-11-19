from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Sum
from .models import StudySession


def get_user_streak(user):
    """
    Calculates consecutive study days for the given user.
    If the user studied today or yesterday, streak is maintained.
    Returns integer streak count.
    """
    sessions = StudySession.objects.filter(user=user).order_by('-start')
    if not sessions.exists():
        return 0

    # Get sorted unique dates (in user's local date or UTC)
    study_dates = set()
    for s in sessions:
        study_dates.add(s.start.date())

    sorted_dates = sorted(list(study_dates), reverse=True)
    if not sorted_dates:
        return 0

    today = date.today()
    yesterday = today - timedelta(days=1)

    most_recent = sorted_dates[0]
    if most_recent != today and most_recent != yesterday:
        # Streak broken
        return 0

    streak = 0
    current_check = most_recent

    for d in sorted_dates:
        if d == current_check:
            streak += 1
            current_check = current_check - timedelta(days=1)
        elif d < current_check:
            # Missed a day
            break

    return streak


def get_study_time_summary(user):
    """
    Returns today's, this week's, and this month's study hours.
    """
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    today_minutes = StudySession.objects.filter(
        user=user,
        start__date=today
    ).aggregate(total=Sum('duration_minutes'))['total'] or 0

    week_minutes = StudySession.objects.filter(
        user=user,
        start__date__gte=start_of_week
    ).aggregate(total=Sum('duration_minutes'))['total'] or 0

    month_minutes = StudySession.objects.filter(
        user=user,
        start__date__gte=start_of_month
    ).aggregate(total=Sum('duration_minutes'))['total'] or 0

    all_time_minutes = StudySession.objects.filter(
        user=user
    ).aggregate(total=Sum('duration_minutes'))['total'] or 0

    return {
        'today_minutes': today_minutes,
        'today_hours': round(today_minutes / 60.0, 1),
        'week_minutes': week_minutes,
        'week_hours': round(week_minutes / 60.0, 1),
        'month_minutes': month_minutes,
        'month_hours': round(month_minutes / 60.0, 1),
        'all_time_hours': round(all_time_minutes / 60.0, 1),
    }
