from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    institution = models.CharField(max_length=200, blank=True, default='')
    course_grade = models.CharField(max_length=100, blank=True, default='', verbose_name='Course / Grade')
    daily_study_target_hours = models.DecimalField(
        max_digits=4, decimal_places=1, default=4.0,
        verbose_name='Daily Study Target (Hours)'
    )
    bio = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return None
