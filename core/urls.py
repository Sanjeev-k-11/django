from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Public Showcase & Landing
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Subjects
    path('subjects/', views.subject_list_view, name='subject_list'),
    path('subjects/create/', views.subject_create_view, name='subject_create'),
    path('subjects/<int:pk>/', views.subject_detail_view, name='subject_detail'),
    path('subjects/<int:pk>/edit/', views.subject_update_view, name='subject_update'),
    path('subjects/<int:pk>/delete/', views.subject_delete_view, name='subject_delete'),
    path('subjects/<int:pk>/toggle-archive/', views.subject_toggle_archive_view, name='subject_toggle_archive'),

    # Assignments
    path('assignments/', views.assignment_list_view, name='assignment_list'),
    path('assignments/create/', views.assignment_create_view, name='assignment_create'),
    path('assignments/<int:pk>/', views.assignment_detail_view, name='assignment_detail'),
    path('assignments/<int:pk>/edit/', views.assignment_update_view, name='assignment_update'),
    path('assignments/<int:pk>/delete/', views.assignment_delete_view, name='assignment_delete'),
    path('assignments/<int:pk>/toggle-status/', views.assignment_toggle_status_ajax, name='assignment_toggle_status'),

    # Subtasks
    path('assignments/<int:assignment_pk>/subtasks/add/', views.subtask_add_ajax, name='subtask_add'),
    path('subtasks/<int:pk>/toggle/', views.subtask_toggle_ajax, name='subtask_toggle'),
    path('subtasks/<int:pk>/delete/', views.subtask_delete_ajax, name='subtask_delete'),

    # Study Goals
    path('goals/', views.goal_list_view, name='goal_list'),
    path('goals/create/', views.goal_create_view, name='goal_create'),
    path('goals/<int:pk>/edit/', views.goal_update_view, name='goal_update'),
    path('goals/<int:pk>/delete/', views.goal_delete_view, name='goal_delete'),
    path('goals/<int:pk>/update-progress/', views.goal_update_progress_ajax, name='goal_update_progress'),

    # Notes
    path('notes/', views.note_list_view, name='note_list'),
    path('notes/create/', views.note_create_view, name='note_create'),
    path('notes/<int:pk>/', views.note_detail_view, name='note_detail'),
    path('notes/<int:pk>/edit/', views.note_update_view, name='note_update'),
    path('notes/<int:pk>/delete/', views.note_delete_view, name='note_delete'),
    path('notes/<int:pk>/toggle-pin/', views.note_toggle_pin, name='note_toggle_pin'),
    path('notes/<int:pk>/download/', views.note_download_txt, name='note_download_txt'),
    path('notes/<int:pk>/print/', views.note_print_view, name='note_print'),

    # Global Search
    path('search/', views.global_search_view, name='global_search'),
]
