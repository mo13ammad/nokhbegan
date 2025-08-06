from django.db import models
from django.conf import settings
from django_jalali.db import models as jmodels

class TuitionFee(models.Model):
    class Status(models.TextChoices):
        UNPAID = 'UNPAID', 'Unpaid'
        PARTIALLY_PAID = 'PARTIALLY_PAID', 'Partially Paid'
        PAID = 'PAID', 'Paid'

    enrollment = models.OneToOneField('enrollment.Enrollment', on_delete=models.CASCADE, related_name='tuition_fee')
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNPAID)
    issue_date = jmodels.jDateField(auto_now_add=True)
    due_date = jmodels.jDateField()

    def __str__(self):
        return f"Tuition for {self.enrollment} - Amount: {self.total_amount}"

    def update_status(self):
        if self.amount_paid >= self.total_amount:
            self.status = self.Status.PAID
        elif self.amount_paid > 0:
            self.status = self.Status.PARTIALLY_PAID
        else:
            self.status = self.Status.UNPAID
        self.save()

class Payment(models.Model):
    class Gateway(models.TextChoices):
        ZARINPAL = 'ZARINPAL', 'Zarinpal'
        DIGIPAY = 'DIGIPAY', 'Digipay'
        MANUAL = 'MANUAL', 'Manual' # For cash, card reader, etc.

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESSFUL = 'SUCCESSFUL', 'Successful'
        FAILED = 'FAILED', 'Failed'

    tuition_fee = models.ForeignKey(TuitionFee, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    payment_gateway = models.CharField(max_length=20, choices=Gateway.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_date = jmodels.jDateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, help_text="Gateway's transaction ID")

    # Who processed the payment (for manual entries)
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'profile__role': 'ADMIN'}
    )

    def __str__(self):
        return f"Payment of {self.amount} for {self.tuition_fee}"

class Installment(models.Model):
    tuition_fee = models.ForeignKey(TuitionFee, on_delete=models.CASCADE, related_name='installments')
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    due_date = jmodels.jDateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Installment of {self.amount} for {self.tuition_fee} due {self.due_date}"

    class Meta:
        ordering = ['due_date']

class Payroll(models.Model):
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payrolls',
        limit_choices_to={'profile__role': 'TEACHER'}
    )
    pay_period_start = jmodels.jDateField()
    pay_period_end = jmodels.jDateField()

    gross_salary = models.DecimalField(max_digits=10, decimal_places=0)
    tax_deduction = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    insurance_deduction = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    benefits = models.DecimalField(max_digits=10, decimal_places=0, default=0, help_text="Housing, food, etc.")
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    net_salary = models.DecimalField(max_digits=10, decimal_places=0)

    issue_date = jmodels.jDateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payroll for {self.instructor.get_full_name()} for period {self.pay_period_start} to {self.pay_period_end}"

    class Meta:
        ordering = ['-pay_period_end']
