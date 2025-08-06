from django.contrib import admin
from .models import Enrollment, Attendance
from jalali_date.admin import ModelAdminJalaliMixin

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0

@admin.register(Enrollment)
class EnrollmentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('student', 'enrolled_class', 'enrollment_date', 'is_active')
    list_filter = ('enrolled_class', 'is_active')
    search_fields = ('student__username', 'enrolled_class__title')
    autocomplete_fields = ('student', 'enrolled_class')
    inlines = [AttendanceInline]

@admin.register(Attendance)
class AttendanceAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('enrollment', 'session_date', 'status')
    list_filter = ('status', 'session_date')
    search_fields = ('enrollment__student__username', 'enrollment__enrolled_class__title')
    autocomplete_fields = ('enrollment',)
