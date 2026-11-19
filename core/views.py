import random
import json
from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Sum, Q, Count

from .models import Subject, StudyGoal, Assignment, Note, ChecklistItem
from .forms import SubjectForm, AssignmentForm, StudyGoalForm, NoteForm, ChecklistItemForm
from planner.models import Exam, TimetableEntry, StudySession, Reminder
from planner.utils import get_user_streak, get_study_time_summary


MOTIVATIONAL_QUOTES = [
    {"quote": "Success is the sum of small efforts, repeated day in and day out.", "author": "Robert Collier"},
    {"quote": "The secret of getting ahead is getting started.", "author": "Mark Twain"},
    {"quote": "Education is the most powerful weapon which you can use to change the world.", "author": "Nelson Mandela"},
    {"quote": "It always seems impossible until it's done.", "author": "Nelson Mandela"},
    {"quote": "Live as if you were to die tomorrow. Learn as if you were to live forever.", "author": "Mahatma Gandhi"},
    {"quote": "Discipline is the bridge between goals and accomplishment.", "author": "Jim Rohn"},
    {"quote": "There are no secrets to success. It is the result of preparation, hard work, and learning from failure.", "author": "Colin Powell"},
    {"quote": "The expert in anything was once a beginner.", "author": "Helen Hayes"},
]


def get_greeting(first_name):
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    return f"{greeting}, {first_name or 'Scholar'} 👋"


def home_view(request):
    """
    Public luxury landing page inspired by modern high-end editorial UI:
    Hero banner carousel, Study categories grid, feature highlights, student reviews.
    """
    categories = [
        {
            'title': 'Courses & Subjects',
            'desc': 'Organize enrolled curriculum, instructor syllabi, credit targets, and lecture archives.',
            'icon': 'fa-book-open',
            'color': '#BE185D',
            'bg': '#FDF2F8',
            'url': '/subjects/' if request.user.is_authenticated else '/accounts/login/',
            'action': 'Explore Courses →',
        },
        {
            'title': 'Assignment Deadlines',
            'desc': 'Interactive milestone checklists, priority labels, overdue alerts, and submission storage.',
            'icon': 'fa-list-check',
            'color': '#0D9488',
            'bg': '#F0FDFA',
            'url': '/assignments/' if request.user.is_authenticated else '/accounts/login/',
            'action': 'View Tasks →',
        },
        {
            'title': 'Pomodoro Study Timer',
            'desc': 'Scientific 25/5 interval focus cycles, interval audio alerts, and automatic session logging.',
            'icon': 'fa-stopwatch',
            'color': '#2563EB',
            'bg': '#EFF6FF',
            'url': '/timer/' if request.user.is_authenticated else '/accounts/login/',
            'action': 'Start Timer →',
        },
        {
            'title': 'Study Streaks',
            'desc': 'Daily continuity tracking, momentum preservation, and study habit analytics.',
            'icon': 'fa-fire',
            'color': '#DC2626',
            'bg': '#FEF2F2',
            'url': '/dashboard/' if request.user.is_authenticated else '/accounts/login/',
            'action': 'Track Habits →',
        },
        {
            'title': 'Weekly Timetable',
            'desc': 'Full recurring weekly class grid, lab schedules, professor office hours, and classrooms.',
            'icon': 'fa-calendar-week',
            'color': '#7C3AED',
            'bg': '#F5F3FF',
            'url': '/timetable/' if request.user.is_authenticated else '/accounts/login/',
            'action': 'See Schedule →',
        },
        {
            'title': 'Exams & GPA Tracker',
            'desc': 'Test day countdowns, score entry, grade projection, and 4.0 weighted GPA calculation.',
            'icon': 'fa-graduation-cap',
            'color': '#D97706',
            'bg': '#FFFBEB',
            'url': '/exams/' if request.user.is_authenticated else '/accounts/login/',
            'action': 'Exams & GPA →',
        },
        {
            'title': 'Study Notes & Formulas',
            'desc': 'Clean revision sheets, pinned formulas, tag exploration, print view, and .txt export.',
            'icon': 'fa-note-sticky',
            'color': '#059669',
            'bg': '#ECFDF5',
            'url': '/notes/' if request.user.is_authenticated else '/accounts/login/',
            'action': 'Browse Notes →',
        },
    ]

    reviews = [
        {
            'name': 'Priya Nair',
            'role': 'Computer Science, IIT Bombay',
            'text': 'StudyMate replaced three different apps for me. The Pomodoro logger tied to my courses kept me in the top 5% of my class.',
            'rating': 5,
        },
        {
            'name': 'Alexander Wright',
            'role': 'Pre-Med, Johns Hopkins University',
            'text': 'The exam countdowns and assignment subtasks kept my clinical lab reports organized and stress-free throughout midterms.',
            'rating': 5,
        },
        {
            'name': 'Simran Kaur',
            'role': 'Applied Mathematics, Imperial College',
            'text': 'The aesthetic is so peaceful, focused, and elegant. You actually want to open StudyMate every morning and plan your day.',
            'rating': 5,
        },
    ]

    context = {
        'categories': categories,
        'reviews': reviews,
        'active_nav': 'home',
        'title': 'StudyMate – Elevate Your Academic Success',
    }
    return render(request, 'core/home.html', context)


def about_view(request):
    """
    Public About Us page detailing StudyMate philosophy, mission, and study methodology.
    """
    context = {
        'active_nav': 'about',
        'title': 'About StudyMate – Philosophy & Academic Mission',
    }
    return render(request, 'core/about.html', context)


def contact_view(request):
    """
    Public Contact & Support page with FAQ and academic assistance.
    """
    context = {
        'active_nav': 'contact',
        'title': 'Academic Support & Contact',
    }
    return render(request, 'core/contact.html', context)


@login_required
def dashboard_view(request):
    user = request.user
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    # Subjects
    subjects = Subject.objects.filter(user=user, is_archived=False)
    subjects_count = subjects.count()

    # Assignments
    assignments = Assignment.objects.filter(user=user).select_related('subject')
    total_assignments_count = assignments.count()
    completed_assignments_count = assignments.filter(status='completed').count()
    pending_assignments_count = assignments.filter(status__in=['not_started', 'in_progress']).count()

    # Goals
    goals = StudyGoal.objects.filter(user=user)
    active_goals_count = goals.filter(status__in=['pending', 'in_progress']).count()
    completed_goals_count = goals.filter(status='completed').count()

    # Study Stats & Streak
    streak = get_user_streak(user)
    study_stats = get_study_time_summary(user)

    # Overall Progress
    total_items = total_assignments_count + goals.count()
    done_items = completed_assignments_count + completed_goals_count
    overall_progress = int((done_items / total_items * 100)) if total_items > 0 else 0

    # Overdue and Upcoming Deadlines (next 5)
    overdue_assignments = assignments.filter(
        due_date__lt=today, status__in=['not_started', 'in_progress']
    ).order_by('due_date')

    upcoming_deadlines = assignments.filter(
        due_date__gte=today, status__in=['not_started', 'in_progress']
    ).order_by('due_date', 'due_time')[:5]

    # Today's Timetable classes
    today_weekday = today.weekday()  # 0=Monday
    today_classes = TimetableEntry.objects.filter(
        user=user, day_of_week=today_weekday
    ).select_related('subject').order_by('start_time')

    # Upcoming Exams (next 3)
    upcoming_exams = Exam.objects.filter(
        user=user, date__gte=today
    ).select_related('subject').order_by('date')[:3]

    # Recent Notes (latest 3)
    recent_notes = Note.objects.filter(user=user).select_related('subject').order_by('-updated_at')[:3]

    # Active Reminders (next 4)
    active_reminders = Reminder.objects.filter(user=user, is_done=False).order_by('datetime')[:4]

    # Chart 1: Assignment Status (Doughnut)
    not_started_count = assignments.filter(status='not_started').count()
    in_progress_count = assignments.filter(status='in_progress').count()
    chart_status_data = [completed_assignments_count, in_progress_count, not_started_count]

    # Chart 2: Study Hours Last 7 Days (Bar)
    last_7_days_labels = []
    last_7_days_hours = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_name = day.strftime('%a')  # Mon, Tue...
        mins = StudySession.objects.filter(
            user=user, start__date=day
        ).aggregate(total=Sum('duration_minutes'))['total'] or 0
        last_7_days_labels.append(day_name)
        last_7_days_hours.append(round(mins / 60.0, 1))

    # Chart 3: Study Time per Subject (Pie)
    subject_time_labels = []
    subject_time_hours = []
    subject_colors = []
    for s in subjects:
        mins = s.total_study_minutes
        if mins > 0:
            subject_time_labels.append(s.name)
            subject_time_hours.append(round(mins / 60.0, 1))
            subject_colors.append(s.color)

    # Motivational Quote
    daily_quote = random.choice(MOTIVATIONAL_QUOTES)

    context = {
        'greeting': get_greeting(user.first_name),
        'daily_quote': daily_quote,
        'subjects_count': subjects_count,
        'active_goals_count': active_goals_count,
        'pending_assignments_count': pending_assignments_count,
        'completed_assignments_count': completed_assignments_count,
        'week_study_hours': study_stats['week_hours'],
        'streak': streak,
        'overall_progress': overall_progress,
        'overdue_assignments': overdue_assignments,
        'upcoming_deadlines': upcoming_deadlines,
        'today_classes': today_classes,
        'upcoming_exams': upcoming_exams,
        'recent_notes': recent_notes,
        'active_reminders': active_reminders,
        'chart_status_data': json.dumps(chart_status_data),
        'chart_days_labels': json.dumps(last_7_days_labels),
        'chart_days_data': json.dumps(last_7_days_hours),
        'chart_subject_labels': json.dumps(subject_time_labels),
        'chart_subject_data': json.dumps(subject_time_hours),
        'chart_subject_colors': json.dumps(subject_colors),
        'active_nav': 'dashboard',
    }
    return render(request, 'core/dashboard.html', context)


# ==========================================================
# SUBJECTS
# ==========================================================
@login_required
def subject_list_view(request):
    show_archived = request.GET.get('archived') == '1'
    subjects = Subject.objects.filter(user=request.user, is_archived=show_archived)

    context = {
        'subjects': subjects,
        'show_archived': show_archived,
        'active_nav': 'subjects',
        'title': 'Archived Subjects' if show_archived else 'My Subjects',
    }
    return render(request, 'core/subject_list.html', context)


@login_required
def subject_create_view(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            messages.success(request, f"Subject '{subject.name}' created successfully!")
            return redirect('core:subject_detail', pk=subject.pk)
    else:
        form = SubjectForm()

    return render(request, 'core/subject_form.html', {'form': form, 'title': 'Add New Subject', 'active_nav': 'subjects'})


@login_required
def subject_detail_view(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    assignments = subject.assignments.all()
    goals = subject.goals.all()
    notes = subject.notes.all()
    exams = subject.exams.all()
    timetable = subject.timetable_entries.all()
    recent_sessions = subject.study_sessions.all()[:5]

    context = {
        'subject': subject,
        'assignments': assignments,
        'goals': goals,
        'notes': notes,
        'exams': exams,
        'timetable': timetable,
        'recent_sessions': recent_sessions,
        'active_nav': 'subjects',
        'title': subject.name,
    }
    return render(request, 'core/subject_detail.html', context)


@login_required
def subject_update_view(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, f"Subject '{subject.name}' updated successfully!")
            return redirect('core:subject_detail', pk=subject.pk)
    else:
        form = SubjectForm(instance=subject)

    return render(request, 'core/subject_form.html', {'form': form, 'title': f'Edit {subject.name}', 'active_nav': 'subjects'})


@login_required
def subject_delete_view(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == 'POST':
        name = subject.name
        subject.delete()
        messages.success(request, f"Subject '{name}' has been deleted.")
        return redirect('core:subject_list')
    return render(request, 'core/confirm_delete.html', {'object': subject, 'type': 'Subject', 'cancel_url': 'core:subject_list'})


@login_required
def subject_toggle_archive_view(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    subject.is_archived = not subject.is_archived
    subject.save()
    status_str = "archived" if subject.is_archived else "restored"
    messages.success(request, f"Subject '{subject.name}' has been {status_str}.")
    return redirect('core:subject_list')


# ==========================================================
# ASSIGNMENTS
# ==========================================================
@login_required
def assignment_list_view(request):
    user = request.user
    queryset = Assignment.objects.filter(user=user).select_related('subject')

    # Filters
    subject_id = request.GET.get('subject')
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    search = request.GET.get('q')
    sort = request.GET.get('sort', 'due_date')

    if subject_id:
        queryset = queryset.filter(subject_id=subject_id)
    if status:
        queryset = queryset.filter(status=status)
    if priority:
        queryset = queryset.filter(priority=priority)
    if search:
        queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

    if sort == 'priority':
        queryset = queryset.order_by('-priority', 'due_date')
    elif sort == 'due_date_desc':
        queryset = queryset.order_by('-due_date')
    elif sort == 'title':
        queryset = queryset.order_by('title')
    else:
        queryset = queryset.order_by('due_date', 'due_time')

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    subjects = Subject.objects.filter(user=user, is_archived=False)

    context = {
        'page_obj': page_obj,
        'subjects': subjects,
        'selected_subject': subject_id,
        'selected_status': status,
        'selected_priority': priority,
        'selected_sort': sort,
        'search_query': search or '',
        'active_nav': 'assignments',
        'title': 'Assignments & Deadlines',
    }
    return render(request, 'core/assignment_list.html', context)


@login_required
def assignment_create_view(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            assignment.save()
            
            # Optional subtasks from form
            subtasks_text = request.POST.get('subtasks_bulk')
            if subtasks_text:
                for line in subtasks_text.splitlines():
                    clean_line = line.strip()
                    if clean_line:
                        ChecklistItem.objects.create(assignment=assignment, title=clean_line)

            messages.success(request, f"Assignment '{assignment.title}' created successfully!")
            return redirect('core:assignment_detail', pk=assignment.pk)
    else:
        form = AssignmentForm(user=request.user)

    return render(request, 'core/assignment_form.html', {'form': form, 'title': 'Create New Assignment', 'active_nav': 'assignments'})


@login_required
def assignment_detail_view(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    subtasks = assignment.subtasks.all()
    subtask_form = ChecklistItemForm()

    context = {
        'assignment': assignment,
        'subtasks': subtasks,
        'subtask_form': subtask_form,
        'active_nav': 'assignments',
        'title': assignment.title,
    }
    return render(request, 'core/assignment_detail.html', context)


@login_required
def assignment_update_view(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Assignment '{assignment.title}' updated successfully!")
            return redirect('core:assignment_detail', pk=assignment.pk)
    else:
        form = AssignmentForm(instance=assignment, user=request.user)

    return render(request, 'core/assignment_form.html', {'form': form, 'title': f'Edit {assignment.title}', 'active_nav': 'assignments'})


@login_required
def assignment_delete_view(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    if request.method == 'POST':
        title = assignment.title
        assignment.delete()
        messages.success(request, f"Assignment '{title}' deleted.")
        return redirect('core:assignment_list')
    return render(request, 'core/confirm_delete.html', {'object': assignment, 'type': 'Assignment', 'cancel_url': 'core:assignment_list'})


@login_required
def assignment_toggle_status_ajax(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    if assignment.status == 'completed':
        assignment.status = 'not_started'
        assignment.completed_at = None
    else:
        assignment.status = 'completed'
        assignment.completed_at = timezone.now()
    assignment.save()

    return JsonResponse({
        'success': True,
        'status': assignment.status,
        'is_completed': assignment.is_completed,
        'countdown_text': assignment.countdown_text,
    })


# ==========================================================
# CHECKLIST / SUBTASKS (AJAX)
# ==========================================================
@login_required
def subtask_add_ajax(request, assignment_pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    assignment = get_object_or_404(Assignment, pk=assignment_pk, user=request.user)
    title = request.POST.get('title', '').strip()
    if not title:
        return JsonResponse({'error': 'Title is required'}, status=400)

    item = ChecklistItem.objects.create(assignment=assignment, title=title)
    return JsonResponse({
        'success': True,
        'id': item.id,
        'title': item.title,
        'is_done': item.is_done,
        'progress_percent': assignment.subtasks_progress_percent,
        'subtasks_done': assignment.subtasks_done_count,
        'subtasks_total': assignment.subtasks_count,
    })


@login_required
def subtask_toggle_ajax(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    item = get_object_or_404(ChecklistItem, pk=pk)
    # verify ownership via assignment or goal
    if item.assignment and item.assignment.user != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    if item.goal and item.goal.user != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    item.is_done = not item.is_done
    item.save()

    progress = 0
    if item.assignment:
        progress = item.assignment.subtasks_progress_percent

    return JsonResponse({
        'success': True,
        'is_done': item.is_done,
        'progress_percent': progress,
    })


@login_required
def subtask_delete_ajax(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    item = get_object_or_404(ChecklistItem, pk=pk)
    if item.assignment and item.assignment.user != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    if item.goal and item.goal.user != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    assignment = item.assignment
    item.delete()

    progress = assignment.subtasks_progress_percent if assignment else 0
    return JsonResponse({'success': True, 'progress_percent': progress})


# ==========================================================
# STUDY GOALS
# ==========================================================
@login_required
def goal_list_view(request):
    user = request.user
    goals = StudyGoal.objects.filter(user=user).select_related('subject')

    goal_type = request.GET.get('type')
    if goal_type in ['daily', 'weekly', 'long_term']:
        goals = goals.filter(goal_type=goal_type)

    status = request.GET.get('status')
    if status:
        goals = goals.filter(status=status)

    context = {
        'goals': goals,
        'selected_type': goal_type or 'all',
        'selected_status': status or 'all',
        'active_nav': 'goals',
        'title': 'Study Goals & Objectives',
    }
    return render(request, 'core/goal_list.html', context)


@login_required
def goal_create_view(request):
    if request.method == 'POST':
        form = StudyGoalForm(request.POST, user=request.user)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            if goal.progress == 100:
                goal.status = 'completed'
            goal.save()
            messages.success(request, f"Study goal '{goal.title}' added successfully!")
            return redirect('core:goal_list')
    else:
        form = StudyGoalForm(user=request.user)

    return render(request, 'core/goal_form.html', {'form': form, 'title': 'Create Study Goal', 'active_nav': 'goals'})


@login_required
def goal_update_view(request, pk):
    goal = get_object_or_404(StudyGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = StudyGoalForm(request.POST, instance=goal, user=request.user)
        if form.is_valid():
            g = form.save(commit=False)
            if g.progress == 100:
                g.status = 'completed'
            g.save()
            messages.success(request, f"Goal '{goal.title}' updated!")
            return redirect('core:goal_list')
    else:
        form = StudyGoalForm(instance=goal, user=request.user)

    return render(request, 'core/goal_form.html', {'form': form, 'title': f'Edit {goal.title}', 'active_nav': 'goals'})


@login_required
def goal_delete_view(request, pk):
    goal = get_object_or_404(StudyGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        title = goal.title
        goal.delete()
        messages.success(request, f"Goal '{title}' deleted.")
        return redirect('core:goal_list')
    return render(request, 'core/confirm_delete.html', {'object': goal, 'type': 'Study Goal', 'cancel_url': 'core:goal_list'})


@login_required
def goal_update_progress_ajax(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    goal = get_object_or_404(StudyGoal, pk=pk, user=request.user)
    try:
        new_progress = int(request.POST.get('progress', 0))
    except ValueError:
        return JsonResponse({'error': 'Invalid progress value'}, status=400)

    goal.progress = max(0, min(100, new_progress))
    if goal.progress == 100:
        goal.status = 'completed'
    elif goal.progress > 0:
        goal.status = 'in_progress'
    else:
        goal.status = 'pending'
    goal.save()

    return JsonResponse({
        'success': True,
        'progress': goal.progress,
        'status': goal.status,
        'status_display': goal.get_status_display(),
    })


# ==========================================================
# NOTES
# ==========================================================
@login_required
def note_list_view(request):
    user = request.user
    notes = Note.objects.filter(user=user).select_related('subject')

    search = request.GET.get('q')
    subject_id = request.GET.get('subject')
    tag = request.GET.get('tag')

    if search:
        notes = notes.filter(Q(title__icontains=search) | Q(content__icontains=search) | Q(tags__icontains=search))
    if subject_id:
        notes = notes.filter(subject_id=subject_id)
    if tag:
        notes = notes.filter(tags__icontains=tag)

    subjects = Subject.objects.filter(user=user, is_archived=False)

    # Collect unique tags
    all_tags = set()
    for n in Note.objects.filter(user=user):
        for t in n.tag_list:
            all_tags.add(t)

    context = {
        'notes': notes,
        'subjects': subjects,
        'all_tags': sorted(list(all_tags)),
        'selected_subject': subject_id,
        'selected_tag': tag,
        'search_query': search or '',
        'active_nav': 'notes',
        'title': 'Study Notes & Knowledge Base',
    }
    return render(request, 'core/note_list.html', context)


@login_required
def note_create_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, f"Note '{note.title}' created successfully!")
            return redirect('core:note_detail', pk=note.pk)
    else:
        form = NoteForm(user=request.user)

    return render(request, 'core/note_form.html', {'form': form, 'title': 'Create Study Note', 'active_nav': 'notes'})


@login_required
def note_detail_view(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    context = {
        'note': note,
        'active_nav': 'notes',
        'title': note.title,
    }
    return render(request, 'core/note_detail.html', context)


@login_required
def note_update_view(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Note '{note.title}' updated successfully!")
            return redirect('core:note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note, user=request.user)

    return render(request, 'core/note_form.html', {'form': form, 'title': f'Edit {note.title}', 'active_nav': 'notes'})


@login_required
def note_delete_view(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        title = note.title
        note.delete()
        messages.success(request, f"Note '{title}' deleted.")
        return redirect('core:note_list')
    return render(request, 'core/confirm_delete.html', {'object': note, 'type': 'Note', 'cancel_url': 'core:note_list'})


@login_required
def note_toggle_pin(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_pinned = not note.is_pinned
    note.save()
    status_str = "pinned to top" if note.is_pinned else "unpinned"
    messages.success(request, f"Note '{note.title}' {status_str}.")
    return redirect('core:note_list')


@login_required
def note_download_txt(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    subject_name = note.subject.name if note.subject else "General"
    file_content = f"Title: {note.title}\n"
    file_content += f"Subject: {subject_name}\n"
    file_content += f"Date: {note.created_at.strftime('%Y-%m-%d %H:%M')}\n"
    file_content += f"Tags: {note.tags}\n"
    file_content += "=" * 50 + "\n\n"
    file_content += note.content

    response = HttpResponse(file_content, content_type='text/plain; charset=utf-8')
    filename = f"{note.title.replace(' ', '_')[:30]}_notes.txt"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def note_print_view(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'core/note_print.html', {'note': note})


# ==========================================================
# GLOBAL SEARCH
# ==========================================================
@login_required
def global_search_view(request):
    query = request.GET.get('q', '').strip()
    subjects = []
    assignments = []
    goals = []
    notes = []

    if query:
        user = request.user
        subjects = Subject.objects.filter(
            user=user
        ).filter(Q(name__icontains=query) | Q(code__icontains=query) | Q(teacher__icontains=query))

        assignments = Assignment.objects.filter(
            user=user
        ).filter(Q(title__icontains=query) | Q(description__icontains=query)).select_related('subject')

        goals = StudyGoal.objects.filter(
            user=user
        ).filter(Q(title__icontains=query) | Q(description__icontains=query)).select_related('subject')

        notes = Note.objects.filter(
            user=user
        ).filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__icontains=query)).select_related('subject')

    total_results = len(subjects) + len(assignments) + len(goals) + len(notes)

    context = {
        'query': query,
        'subjects': subjects,
        'assignments': assignments,
        'goals': goals,
        'notes': notes,
        'total_results': total_results,
        'active_nav': '',
        'title': f'Search Results for "{query}"',
    }
    return render(request, 'core/global_search.html', context)
