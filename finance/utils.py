"""
Utilities for financial calculations, specifically for teacher salary.
The parameters are based on the SRS document (AGENTS.md), Table 3.7.1 for the year 1403.
"""
from decimal import Decimal
from django.contrib.auth.models import User
from courses.models import Class
from datetime import date, timedelta

# --- Legal Parameters for Salary Calculation (Year 1403) ---
# NOTE: In a production system, these should be stored in the database
# or a settings file to be easily updatable by an admin.

# Monthly amounts in Rials
HOUSING_BENEFIT = Decimal('9000000')
FOOD_BENEFIT = Decimal('14000000')
MARRIAGE_BENEFIT = Decimal('5000000')
CHILD_BENEFIT_PER_CHILD = Decimal('7166184')

# Daily amounts
MINIMUM_DAILY_WAGE = Decimal('2388728')
YEARS_OF_SERVICE_DAILY_BENEFIT = Decimal('70000') # For employees with >1 year of service

# Percentages
INSURANCE_DEDUCTION_RATE = Decimal('0.07') # 7% employee share
OVERTIME_RATE = Decimal('1.4') # 140%

# Tax brackets (monthly, in Rials)
TAX_BRACKETS = [
    {'limit': Decimal('120000000'), 'rate': Decimal('0.00')},
    {'limit': Decimal('165000000'), 'rate': Decimal('0.10')},
    {'limit': Decimal('270000000'), 'rate': Decimal('0.15')},
    {'limit': Decimal('400000000'), 'rate': Decimal('0.20')},
    # Assuming any amount above 400M Rials is taxed at 30%
    {'limit': float('inf'), 'rate': Decimal('0.30')},
]

def calculate_monthly_tax(monthly_income: Decimal) -> Decimal:
    """Calculates progressive income tax based on the defined brackets."""
    tax = Decimal('0')
    previous_limit = Decimal('0')

    for bracket in TAX_BRACKETS:
        if monthly_income > previous_limit:
            taxable_at_this_rate = min(monthly_income, bracket['limit']) - previous_limit
            tax += taxable_at_this_rate * bracket['rate']
            previous_limit = bracket['limit']
        else:
            break

    return tax

def calculate_teacher_salary(instructor: User, pay_period_start: date, pay_period_end: date) -> dict:
    """
    Calculates a teacher's salary for a given period.
    This is a simplified model assuming hourly pay.
    """
    if not instructor.profile.role == 'TEACHER':
        return {"error": "User is not a teacher."}

    # 1. Calculate total hours worked in the period
    # This is a simplified calculation. A real system would need to track actual class sessions held.
    total_hours = 0
    instructor_classes = Class.objects.filter(instructor=instructor)

    # Assuming a simple hourly rate is stored somewhere, e.g., on the profile.
    # For this simulation, we'll use a placeholder hourly rate.
    hourly_rate = Decimal('500000') # Placeholder: 500,000 Rials per hour

    # A more accurate way would be to count sessions within the date range
    # For now, we estimate based on weekly schedule
    num_weeks = (pay_period_end - pay_period_start).days / 7
    for klass in instructor_classes:
        class_duration_hours = (klass.end_time.hour - klass.start_time.hour) + \
                               (klass.end_time.minute - klass.start_time.minute) / 60
        num_sessions_per_week = len(klass.days_of_week.split(','))
        total_hours += num_sessions_per_week * class_duration_hours * num_weeks

    # 2. Calculate Gross Salary
    gross_salary = total_hours * hourly_rate

    # 3. Add Legal Benefits
    # This is a simplified calculation. A full implementation would check for conditions.
    benefits_total = HOUSING_BENEFIT + FOOD_BENEFIT
    # Example: Check if married
    # if instructor.profile.is_married:
    #     benefits_total += MARRIAGE_BENEFIT

    income_before_tax = gross_salary + benefits_total

    # 4. Calculate Deductions
    # Insurance is typically calculated on a base salary + some benefits, not all.
    # This is a simplification.
    insurance_base = gross_salary
    insurance_deduction = insurance_base * INSURANCE_DEDUCTION_RATE

    # Tax is calculated on income after insurance deduction
    taxable_income = income_before_tax - insurance_deduction
    tax_deduction = calculate_monthly_tax(taxable_income)

    # 5. Calculate Net Salary
    net_salary = income_before_tax - insurance_deduction - tax_deduction

    return {
        "gross_salary": gross_salary,
        "benefits_total": benefits_total,
        "income_before_tax": income_before_tax,
        "insurance_deduction": insurance_deduction,
        "tax_deduction": tax_deduction,
        "net_salary": net_salary,
        "pay_period_start": pay_period_start,
        "pay_period_end": pay_period_end,
        "calculation_details": {
            "total_hours_estimated": total_hours,
            "hourly_rate": hourly_rate,
        }
    }
