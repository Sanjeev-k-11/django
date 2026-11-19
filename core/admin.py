from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Subject, StudyGoal, Assignment, ChecklistItem, Note


class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 1
    fields = ('title', 'is_done')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('color_badge', 'name', 'code', 'user', 'teacher', 'target_grade', 'assignments_summary', 'is_archived')
    list_filter = ('is_archived', 'created_at', 'user')
    search_fields = ('name', 'code', 'teacher', 'user__username')
    ordering = ('name',)

    @admin.display(description='Theme Color')
    def color_badge(self, obj):
        return format_html(
            '<div style="display:flex; align-items:center; gap:6px;">'
            '<span style="display:inline-block; width:14px; height:14px; border-radius:50%; background-color:{}; border:1px solid #ccc;"></span>'
            '<code>{}</code></div>',
            obj.color, obj.color
        )

    @admin.display(description='Tasks Completed')
    def assignments_summary(self, obj):
        total = obj.total_assignments
        done = obj.completed_assignments
        pct = obj.assignment_progress
        return format_html('<b>{}/{}</b> ({}%)', done, total, pct)


@admin.register(StudyGoal)
class StudyGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'subject', 'goal_type_badge', 'target_date', 'status_badge', 'progress_bar')
    list_filter = ('goal_type', 'status', 'target_date', 'user')
    search_fields = ('title', 'description', 'user__username')
    inlines = [ChecklistItemInline]

    @admin.display(description='Type')
    def goal_type_badge(self, obj):
        return format_html('<span style="padding:2px 8px; border-radius:12px; background:#EFF6FF; color:#2563EB; font-weight:bold;">{}</span>', obj.get_goal_type_display())

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {'completed': '#16A34A', 'in_progress': '#2563EB', 'pending': '#F59E0B'}
        return format_html('<span style="color:{}; font-weight:bold;">● {}</span>', colors.get(obj.status, '#666'), obj.get_status_display())

    @admin.display(description='Progress')
    def progress_bar(self, obj):
        return format_html(
            '<div style="width:100px; height:8px; background:#E5E7EB; border-radius:4px; overflow:hidden;">'
            '<div style="width:{}%; height:100%; background:#10B981;"></div>'
            '</div> <span style="font-size:11px;">{}%</span>',
            obj.progress, obj.progress
        )


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject_tag', 'user', 'due_date', 'priority_badge', 'status_badge', 'has_attachment')
    list_filter = ('priority', 'status', 'due_date', 'subject', 'user')
    search_fields = ('title', 'description', 'user__username', 'subject__name')
    inlines = [ChecklistItemInline]

    @admin.display(description='Subject')
    def subject_tag(self, obj):
        return format_html(
            '<span style="padding:2px 8px; border-radius:10px; background:{}20; color:{}; font-weight:bold; border:1px solid {}40;">{}</span>',
            obj.subject.color, obj.subject.color, obj.subject.color, obj.subject.name
        )

    @admin.display(description='Priority')
    def priority_badge(self, obj):
        colors = {'high': '#DC2626', 'medium': '#F59E0B', 'low': '#0D9488'}
        return format_html('<span style="color:{}; font-weight:bold;">{}</span>', colors.get(obj.priority, '#666'), obj.get_priority_display())

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.is_completed:
            return mark_safe('<span style="color:#16A34A; font-weight:bold;">✓ Completed</span>')
        elif obj.is_overdue:
            return mark_safe('<span style="color:#DC2626; font-weight:bold;">⚠ Overdue</span>')
        return format_html('<span style="color:#2563EB;">{}</span>', obj.get_status_display())

    @admin.display(description='File', boolean=True)
    def has_attachment(self, obj):
        return bool(obj.attachment)


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'assignment', 'goal', 'is_done_badge', 'created_at')
    list_filter = ('is_done', 'created_at')
    search_fields = ('title',)

    @admin.display(description='Done', boolean=True)
    def is_done_badge(self, obj):
        return obj.is_done


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'subject', 'pin_badge', 'tag_list_display', 'updated_at')
    list_filter = ('is_pinned', 'created_at', 'subject', 'user')
    search_fields = ('title', 'content', 'tags', 'user__username')

    @admin.display(description='Pinned')
    def pin_badge(self, obj):
        return "📌 Pinned" if obj.is_pinned else "—"

    @admin.display(description='Tags')
    def tag_list_display(self, obj):
        return obj.tags if obj.tags else "-"
