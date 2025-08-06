from django.contrib import admin
from .models import TuitionFee, Payment, Installment, Payroll
from jalali_date.admin import ModelAdminJalaliMixin, TabularInlineJalaliMixin

class PaymentInline(TabularInlineJalaliMixin, admin.TabularInline):
    model = Payment
    extra = 0

class InstallmentInline(TabularInlineJalaliMixin, admin.TabularInline):
    model = Installment
    extra = 0

@admin.register(TuitionFee)
class TuitionFeeAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('enrollment', 'total_amount', 'amount_paid', 'status', 'due_date')
    list_filter = ('status',)
    search_fields = ('enrollment__student__username', 'enrollment__enrolled_class__title')
    autocomplete_fields = ('enrollment',)
    inlines = [PaymentInline, InstallmentInline]

@admin.register(Payment)
class PaymentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('tuition_fee', 'amount', 'payment_gateway', 'status', 'payment_date')
    list_filter = ('payment_gateway', 'status')
    search_fields = ('tuition_fee__enrollment__student__username',)
    autocomplete_fields = ('tuition_fee', 'processed_by')

@admin.register(Payroll)
class PayrollAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('instructor', 'pay_period_start', 'pay_period_end', 'net_salary', 'is_paid')
    list_filter = ('is_paid', 'instructor')
    search_fields = ('instructor__username',)
    autocomplete_fields = ('instructor',)
