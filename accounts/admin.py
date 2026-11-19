from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Student Profile'
    fk_name = 'user'
    fields = ('avatar', 'institution', 'course_grade', 'daily_study_target_hours', 'bio')


# Re-register UserAdmin to include Profile inline
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_institution', 'get_target_hours', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    @admin.display(description='Institution')
    def get_institution(self, obj):
        return obj.profile.institution if hasattr(obj, 'profile') else '-'

    @admin.display(description='Daily Target')
    def get_target_hours(self, obj):
        return f"{obj.profile.daily_study_target_hours} hrs" if hasattr(obj, 'profile') else '-'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar_preview', 'institution', 'course_grade', 'daily_study_target_hours', 'created_at')
    search_fields = ('user__username', 'user__email', 'institution', 'course_grade')
    list_filter = ('created_at',)

    @admin.display(description='Avatar')
    def avatar_preview(self, obj):
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return format_html('<img src="{}" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover;" />', obj.avatar.url)
        return format_html('<span style="display:inline-block; width:36px; height:36px; border-radius:50%; background:#EFF6FF; color:#2563EB; text-align:center; line-height:36px; font-weight:bold;">{}</span>', obj.user.username[:1].upper())
