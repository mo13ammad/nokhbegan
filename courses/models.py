from django.db import models
from django.conf import settings
from django_jalali.db import models as jmodels

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    syllabus = models.TextField(blank=True, null=True)
    base_tuition_fee = models.DecimalField(max_digits=10, decimal_places=0, help_text="Base tuition fee for the course")

    def __str__(self):
        return self.title

class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='classes')
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='classes_taught',
        limit_choices_to={'profile__role': 'TEACHER'}
    )
    title = models.CharField(max_length=200, help_text="e.g., 'Group A - Mornings'")
    capacity = models.PositiveIntegerField()
    start_date = jmodels.jDateField()
    end_date = jmodels.jDateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    # Using a simple text field for days, can be improved with a ManyToManyField to a Day model if needed
    days_of_week = models.CharField(max_length=100, help_text="e.g., 'Saturday, Monday'")

    custom_tuition_fee = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
        help_text="Override course base fee if needed"
    )

    def get_tuition_fee(self):
        return self.custom_tuition_fee if self.custom_tuition_fee is not None else self.course.base_tuition_fee

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        verbose_name_plural = "Classes"
