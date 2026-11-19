from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_dashboard_view, name='dashboard'),
    path('export/assignments/', views.export_assignments_csv, name='export_assignments_csv'),
    path('export/sessions/', views.export_sessions_csv, name='export_sessions_csv'),
    path('report/', views.printable_progress_report, name='progress_report'),
]
