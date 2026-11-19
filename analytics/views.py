import csv
import json
from datetime import date, datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum, Count, Avg

from core.models import Subject, Assignment, StudyGoal
from planner.models import StudySession, Exam
from planner.utils import get_study_time_summary, get_user_streak


@login_required
def analytics_dashboard_view(request):
    user = request.user
    today = date.today()

    # Study time stats
    study_summary = get_study_time_summary(user)
    streak = get_user_streak(user)

    # 1. Subject-wise time distribution
    subjects = Subject.objects.filter(user=user)
    subject_names = []
    subject_hours = []
    subject_colors = []
    for s in subjects:
        hrs = s.total_study_hours
        if hrs > 0:
            subject_names.append(s.name)
            subject_hours.append(hrs)
            subject_colors.append(s.color)

    # 2. Assignment completion stats
    assignments = Assignment.objects.filter(user=user)
    total_assignments = assignments.count()
    completed_assignments = assignments.filter(status='completed').count()
    overdue_assignments = assignments.filter(due_date__lt=today).exclude(status='completed').count()
    in_progress_assignments = assignments.filter(status='in_progress').count()
    not_started_assignments = assignments.filter(status='not_started').count()

    assignment_rate = int((completed_assignments / total_assignments * 100)) if total_assignments > 0 else 0

    # 3. Goal completion stats
    goals = StudyGoal.objects.filter(user=user)
    total_goals = goals.count()
    completed_goals = goals.filter(status='completed').count()
    goal_rate = int((completed_goals / total_goals * 100)) if total_goals > 0 else 0

    # 4. Weekly study hours over the past 4 weeks
    week_labels = []
    week_hours_data = []
    for w in range(3, -1, -1):
        w_start = today - timedelta(days=today.weekday() + (w * 7))
        w_end = w_start + timedelta(days=6)
        mins = StudySession.objects.filter(
            user=user,
            start__date__gte=w_start,
            start__date__lte=w_end
        ).aggregate(total=Sum('duration_minutes'))['total'] or 0
        week_labels.append(f"Week {4 - w} ({w_start.strftime('%b %d')})")
        week_hours_data.append(round(mins / 60.0, 1))

    # 5. Exam Performance trend
    graded_exams = Exam.objects.filter(
        user=user, marks_obtained__isnull=False, total_marks__isnull=False
    ).order_by('date')
    exam_labels = [f"{e.title} ({e.subject.code or e.subject.name})" for e in graded_exams]
    exam_scores = [e.percentage for e in graded_exams]

    avg_exam_score = round(sum(exam_scores) / len(exam_scores), 1) if exam_scores else None

    context = {
        'study_summary': study_summary,
        'streak': streak,
        'total_assignments': total_assignments,
        'completed_assignments': completed_assignments,
        'overdue_assignments': overdue_assignments,
        'assignment_rate': assignment_rate,
        'total_goals': total_goals,
        'completed_goals': completed_goals,
        'goal_rate': goal_rate,
        'avg_exam_score': avg_exam_score,
        'chart_subject_names': json.dumps(subject_names),
        'chart_subject_hours': json.dumps(subject_hours),
        'chart_subject_colors': json.dumps(subject_colors),
        'chart_week_labels': json.dumps(week_labels),
        'chart_week_hours': json.dumps(week_hours_data),
        'chart_assignment_breakdown': json.dumps([completed_assignments, in_progress_assignments, not_started_assignments, overdue_assignments]),
        'chart_exam_labels': json.dumps(exam_labels),
        'chart_exam_scores': json.dumps(exam_scores),
        'active_nav': 'analytics',
        'title': 'Academic Analytics & Progress',
    }
    return render(request, 'analytics/dashboard.html', context)


@login_required
def export_assignments_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="studymate_assignments_{date.today()}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Subject', 'Due Date', 'Due Time', 'Priority', 'Status', 'Completed At'])

    assignments = Assignment.objects.filter(user=request.user).select_related('subject')
    for a in assignments:
        writer.writerow([
            a.title,
            a.subject.name,
            a.due_date,
            a.due_time or '',
            a.get_priority_display(),
            a.get_status_display(),
            a.completed_at.strftime('%Y-%m-%d %H:%M') if a.completed_at else '',
        ])

    return response


@login_required
def export_sessions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="studymate_study_sessions_{date.today()}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date & Time', 'Subject', 'Duration (Minutes)', 'Duration (Hours)', 'Notes'])

    sessions = StudySession.objects.filter(user=request.user).select_related('subject').order_by('-start')
    for s in sessions:
        writer.writerow([
            s.start.strftime('%Y-%m-%d %H:%M'),
            s.subject.name if s.subject else 'General Study',
            s.duration_minutes,
            s.hours,
            s.notes,
        ])

    return response


@login_required
def printable_progress_report(request):
    user = request.user
    today = date.today()

    study_summary = get_study_time_summary(user)
    streak = get_user_streak(user)
    subjects = Subject.objects.filter(user=user)
    assignments = Assignment.objects.filter(user=user).select_related('subject')
    exams = Exam.objects.filter(user=user).select_related('subject')
    goals = StudyGoal.objects.filter(user=user).select_related('subject')

    total_assignments = assignments.count()
    completed_assignments = assignments.filter(status='completed').count()
    completion_rate = int((completed_assignments / total_assignments * 100)) if total_assignments > 0 else 0

    graded_exams = exams.filter(marks_obtained__isnull=False, total_marks__isnull=False)
    total_obtained = sum(e.marks_obtained for e in graded_exams)
    total_possible = sum(e.total_marks for e in graded_exams)
    overall_percentage = round((total_obtained / total_possible * 100), 1) if total_possible > 0 else None

    overall_gpa = None
    if overall_percentage is not None:
        if overall_percentage >= 90:
            overall_gpa = 4.0
        elif overall_percentage >= 80:
            overall_gpa = 3.5
        elif overall_percentage >= 70:
            overall_gpa = 3.0
        elif overall_percentage >= 60:
            overall_gpa = 2.5
        elif overall_percentage >= 50:
            overall_gpa = 2.0
        else:
            overall_gpa = 1.0

    context = {
        'student': user,
        'profile': user.profile,
        'report_date': today,
        'study_summary': study_summary,
        'streak': streak,
        'subjects': subjects,
        'assignments': assignments,
        'exams': exams,
        'goals': goals,
        'completion_rate': completion_rate,
        'overall_percentage': overall_percentage,
        'overall_gpa': overall_gpa,
    }
    return render(request, 'analytics/progress_report.html', context)
