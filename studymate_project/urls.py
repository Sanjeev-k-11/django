from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Custom Admin Site Branding (SQLite Database Management Portal)
admin.site.site_header = "StudyMate Academic Database Administration"
admin.site.site_title = "StudyMate Admin Portal"
admin.site.index_title = "SQLite Academic Database & System Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('core.urls')),
    path('', include('planner.urls')),
    path('analytics/', include('analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'core.views_errors.custom_404'
handler500 = 'core.views_errors.custom_500'
