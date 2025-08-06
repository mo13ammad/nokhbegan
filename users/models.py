from django.db import models
from django.contrib.auth.models import User
from jalali_date import date2jalali, datetime2jalali

class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        TEACHER = 'TEACHER', 'Teacher'
        STUDENT = 'STUDENT', 'Student'
        PARENT = 'PARENT', 'Parent'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    national_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # For students, this links to their parent's profile
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()}"

    @property
    def created_jalali(self):
        return date2jalali(self.user.date_joined)

    @property
    def last_login_jalali(self):
        if self.user.last_login:
            return datetime2jalali(self.user.last_login)
        return None
