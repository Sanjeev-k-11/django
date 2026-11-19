import json
from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Avg, Sum, Count

from .models import StudySession, Exam, TimetableEntry, Reminder
from .forms import StudySessionForm, ExamForm, TimetableEntryForm, ReminderForm
from .utils import get_study_time_summary, get_user_streak
from core.models import Subject, Assignment, StudyGoal


# ==========================================================
# POMODORO STUDY TIMER
# ==========================================================
@login_required
def timer_view(request):
    user = request.user
    subjects = Subject.objects.filter(user=user, is_archived=False)
    study_summary = get_study_time_summary(user)
    recent_sessions = StudySession.objects.filter(user=user).select_related('subject')[:10]

    context = {
        'subjects': subjects,
        'study_summary': study_summary,
        'recent_sessions': recent_sessions,
        'streak': get_user_streak(user),
        'active_nav': 'timer',
        'title': 'Pomodoro Study Timer',
    }
    return render(request, 'planner/timer.html', context)


@login_required
def timer_log_ajax(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST

    subject_id = data.get('subject_id')
    duration = int(data.get('duration_minutes', 25))
    notes = data.get('notes', '')

    subject = None
    if subject_id:
        subject = get_object_or_404(Subject, pk=subject_id, user=request.user)

    session = StudySession.objects.create(
        user=request.user,
        subject=subject,
        start=timezone.now() - timedelta(minutes=duration),
        duration_minutes=duration,
        notes=notes,
    )

    summary = get_study_time_summary(request.user)
    streak = get_user_streak(request.user)

    return JsonResponse({
        'success': True,
        'session_id': session.id,
        'subject_name': subject.name if subject else "General Study",
        'duration_minutes': session.duration_minutes,
        'today_hours': summary['today_hours'],
        'week_hours': summary['week_hours'],
        'streak': streak,
    })


@login_required
def session_delete_view(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    if request.method == 'POST':
        session.delete()
        messages.success(request, "Study session deleted.")
    return redirect('planner:timer')


# ==========================================================
# CALENDAR & EVENTS JSON API
# ==========================================================
@login_required
def calendar_view(request):
    return render(request, 'planner/calendar.html', {
        'active_nav': 'calendar',
        'title': 'Academic Calendar',
    })


@login_required
def calendar_events_api(request):
    """
    Returns full calendar JSON events for FullCalendar:
    - Assignments (colored by subject or status)
    - Exams (purple/red)
    - Study Goals (teal/green)
    - Reminders (amber)
    """
    user = request.user
    events = []

    # 1. Assignments
    assignments = Assignment.objects.filter(user=user).select_related('subject')
    for a in assignments:
        bg_color = '#16A34A' if a.is_completed else ('#DC2626' if a.is_overdue else (a.subject.color or '#2563EB'))
        start_str = a.due_date.isoformat()
        if a.due_time:
            start_str += f"T{a.due_time.isoformat()}"
        events.append({
            'id': f"assignment_{a.id}",
            'title': f"📝 {a.title} ({a.subject.code or a.subject.name})",
            'start': start_str,
            'url': f"/assignments/{a.id}/",
            'backgroundColor': bg_color,
            'borderColor': bg_color,
            'extendedProps': {
                'type': 'Assignment',
                'status': a.get_status_display(),
                'priority': a.get_priority_display(),
            }
        })

    # 2. Exams
    exams = Exam.objects.filter(user=user).select_related('subject')
    for e in exams:
        start_str = e.date.isoformat()
        if e.time:
            start_str += f"T{e.time.isoformat()}"
        events.append({
            'id': f"exam_{e.id}",
            'title': f"🎓 EXAM: {e.title} ({e.subject.name})",
            'start': start_str,
            'url': f"/exams/{e.id}/edit/",
            'backgroundColor': '#7C3AED',
            'borderColor': '#6D28D9',
            'extendedProps': {
                'type': 'Exam',
                'location': e.location,
            }
        })

    # 3. Goals
    goals = StudyGoal.objects.filter(user=user).select_related('subject')
    for g in goals:
        events.append({
            'id': f"goal_{g.id}",
            'title': f"🎯 Goal: {g.title}",
            'start': g.target_date.isoformat(),
            'url': "/goals/",
            'backgroundColor': '#0D9488',
            'borderColor': '#0F766E',
            'extendedProps': {
                'type': 'Goal',
                'progress': f"{g.progress}%",
            }
        })

    # 4. Reminders
    reminders = Reminder.objects.filter(user=user)
    for r in reminders:
        events.append({
            'id': f"reminder_{r.id}",
            'title': f"🔔 {r.title}",
            'start': r.datetime.isoformat(),
            'url': "/reminders/",
            'backgroundColor': '#F59E0B' if not r.is_done else '#9CA3AF',
            'borderColor': '#D97706' if not r.is_done else '#6B7280',
            'extendedProps': {
                'type': 'Reminder',
                'is_done': r.is_done,
            }
        })

    return JsonResponse(events, safe=False)


# ==========================================================
# TIMETABLE
# ==========================================================
@login_required
def timetable_view(request):
    user = request.user
    entries = TimetableEntry.objects.filter(user=user).select_related('subject').order_by('day_of_week', 'start_time')

    # Group entries by day of week
    days = [
        {'day_index': 0, 'name': 'Monday', 'entries': []},
        {'day_index': 1, 'name': 'Tuesday', 'entries': []},
        {'day_index': 2, 'name': 'Wednesday', 'entries': []},
        {'day_index': 3, 'name': 'Thursday', 'entries': []},
        {'day_index': 4, 'name': 'Friday', 'entries': []},
        {'day_index': 5, 'name': 'Saturday', 'entries': []},
        {'day_index': 6, 'name': 'Sunday', 'entries': []},
    ]

    for e in entries:
        if 0 <= e.day_of_week <= 6:
            days[e.day_of_week]['entries'].append(e)

    subjects = Subject.objects.filter(user=user, is_archived=False)
    form = TimetableEntryForm(user=user)

    context = {
        'days': days,
        'entries': entries,
        'subjects': subjects,
        'form': form,
        'active_nav': 'timetable',
        'title': 'Weekly Class Timetable',
    }
    return render(request, 'planner/timetable.html', context)


@login_required
def timetable_create_view(request):
    if request.method == 'POST':
        form = TimetableEntryForm(request.POST, user=request.user)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, f"Class added to {entry.get_day_of_week_display()} timetable!")
            return redirect('planner:timetable')
        else:
            messages.error(request, "Please check the timetable form errors.")
    return redirect('planner:timetable')


@login_required
def timetable_edit_view(request, pk):
    entry = get_object_or_404(TimetableEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TimetableEntryForm(request.POST, instance=entry, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Timetable entry updated!")
            return redirect('planner:timetable')
    else:
        form = TimetableEntryForm(instance=entry, user=request.user)

    return render(request, 'planner/timetable_form.html', {
        'form': form,
        'entry': entry,
        'active_nav': 'timetable',
        'title': 'Edit Timetable Entry',
    })


@login_required
def timetable_delete_view(request, pk):
    entry = get_object_or_404(TimetableEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, "Class entry removed from timetable.")
        return redirect('planner:timetable')
    return render(request, 'core/confirm_delete.html', {'object': entry, 'type': 'Timetable Class', 'cancel_url': 'planner:timetable'})


# ==========================================================
# EXAMS & GRADES
# ==========================================================
@login_required
def exam_list_view(request):
    user = request.user
    today = date.today()
    exams = Exam.objects.filter(user=user).select_related('subject')

    upcoming_exams = exams.filter(date__gte=today).order_by('date', 'time')
    past_exams = exams.filter(date__lt=today).order_by('-date', '-time')

    # GPA / Average Calculation
    graded_exams = exams.filter(marks_obtained__isnull=False, total_marks__isnull=False)
    total_obtained = sum(e.marks_obtained for e in graded_exams)
    total_possible = sum(e.total_marks for e in graded_exams)
    overall_percentage = round((total_obtained / total_possible * 100), 1) if total_possible > 0 else None

    # Estimate GPA on 4.0 scale
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

    # Subject performance chart data
    subject_marks = {}
    for ge in graded_exams:
        s_name = ge.subject.name
        if s_name not in subject_marks:
            subject_marks[s_name] = []
        subject_marks[s_name].append(ge.percentage)

    chart_subjects = list(subject_marks.keys())
    chart_avg_scores = [round(sum(v)/len(v), 1) for v in subject_marks.values()]

    context = {
        'upcoming_exams': upcoming_exams,
        'past_exams': past_exams,
        'overall_percentage': overall_percentage,
        'overall_gpa': overall_gpa,
        'graded_exams_count': graded_exams.count(),
        'chart_subjects': json.dumps(chart_subjects),
        'chart_avg_scores': json.dumps(chart_avg_scores),
        'active_nav': 'exams',
        'title': 'Exams, Tests & Academic Grades',
    }
    return render(request, 'planner/exam_list.html', context)


@login_required
def exam_create_view(request):
    if request.method == 'POST':
        form = ExamForm(request.POST, user=request.user)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.user = request.user
            exam.save()
            messages.success(request, f"Exam '{exam.title}' added to schedule!")
            return redirect('planner:exam_list')
    else:
        form = ExamForm(user=request.user)

    return render(request, 'planner/exam_form.html', {'form': form, 'title': 'Schedule New Exam', 'active_nav': 'exams'})


@login_required
def exam_edit_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Exam '{exam.title}' updated!")
            return redirect('planner:exam_list')
    else:
        form = ExamForm(instance=exam, user=request.user)

    return render(request, 'planner/exam_form.html', {'form': form, 'title': f'Edit {exam.title}', 'active_nav': 'exams'})


@login_required
def exam_delete_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk, user=request.user)
    if request.method == 'POST':
        title = exam.title
        exam.delete()
        messages.success(request, f"Exam '{title}' deleted.")
        return redirect('planner:exam_list')
    return render(request, 'core/confirm_delete.html', {'object': exam, 'type': 'Exam', 'cancel_url': 'planner:exam_list'})


# ==========================================================
# REMINDERS
# ==========================================================
@login_required
def reminder_list_view(request):
    reminders = Reminder.objects.filter(user=request.user).order_by('is_done', 'datetime')
    form = ReminderForm()

    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request, f"Reminder '{reminder.title}' set!")
            return redirect('planner:reminders')

    context = {
        'reminders': reminders,
        'form': form,
        'active_nav': 'reminders',
        'title': 'Academic Reminders',
    }
    return render(request, 'planner/reminder_list.html', context)


@login_required
def reminder_toggle_ajax(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    reminder.is_done = not reminder.is_done
    reminder.save()

    return JsonResponse({'success': True, 'is_done': reminder.is_done})


@login_required
def reminder_delete_view(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    if request.method == 'POST':
        reminder.delete()
        messages.success(request, "Reminder deleted.")
    return redirect('planner:reminders')
