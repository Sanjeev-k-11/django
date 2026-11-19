from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    # Pomodoro Timer
    path('timer/', views.timer_view, name='timer'),
    path('timer/log/', views.timer_log_ajax, name='timer_log_ajax'),
    path('timer/session/<int:pk>/delete/', views.session_delete_view, name='session_delete'),

    # Calendar
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/events/', views.calendar_events_api, name='calendar_events_api'),

    # Timetable
    path('timetable/', views.timetable_view, name='timetable'),
    path('timetable/create/', views.timetable_create_view, name='timetable_create'),
    path('timetable/<int:pk>/edit/', views.timetable_edit_view, name='timetable_edit'),
    path('timetable/<int:pk>/delete/', views.timetable_delete_view, name='timetable_delete'),

    # Exams
    path('exams/', views.exam_list_view, name='exam_list'),
    path('exams/create/', views.exam_create_view, name='exam_create'),
    path('exams/<int:pk>/edit/', views.exam_edit_view, name='exam_edit'),
    path('exams/<int:pk>/delete/', views.exam_delete_view, name='exam_delete'),

    # Reminders
    path('reminders/', views.reminder_list_view, name='reminders'),
    path('reminders/<int:pk>/toggle/', views.reminder_toggle_ajax, name='reminder_toggle_ajax'),
    path('reminders/<int:pk>/delete/', views.reminder_delete_view, name='reminder_delete'),
]
