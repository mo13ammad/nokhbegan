from django.contrib import admin
from .models import Course, Class
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin

class ClassInline(TabularInlineJalaliMixin, admin.TabularInline):
    model = Class
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'base_tuition_fee')
    search_fields = ('title',)
    inlines = [ClassInline]

@admin.register(Class)
class ClassAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title', 'course', 'instructor', 'start_date', 'end_date', 'capacity')
    list_filter = ('course', 'instructor', 'start_date')
    search_fields = ('title', 'course__title', 'instructor__first_name', 'instructor__last_name')
    autocomplete_fields = ('instructor',)
