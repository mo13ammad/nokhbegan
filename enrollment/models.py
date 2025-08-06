from django.db import models
from django.conf import settings
from django_jalali.db import models as jmodels

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        limit_choices_to={'profile__role': 'STUDENT'}
    )
    enrolled_class = models.ForeignKey('courses.Class', on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = jmodels.jDateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        student_name = self.student.get_full_name() or self.student.username
        return f"{student_name} enrolled in {self.enrolled_class}"

    class Meta:
        unique_together = ('student', 'enrolled_class')

class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'PRESENT', 'Present'
        ABSENT = 'ABSENT', 'Absent'
        LATE = 'LATE', 'Late'

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attendance_records')
    session_date = jmodels.jDateField()
    status = models.CharField(max_length=10, choices=Status.choices)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # Explicitly format the date to ensure consistent output
        date_str = self.session_date.strftime("%Y-%m-%d") if self.session_date else ""
        return f"{self.enrollment} - {date_str} - {self.get_status_display()}"

    class Meta:
        unique_together = ('enrollment', 'session_date')
        ordering = ['-session_date']
