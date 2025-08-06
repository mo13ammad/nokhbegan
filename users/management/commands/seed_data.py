import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from faker import Faker

from users.models import Profile
from courses.models import Course, Class
from enrollment.models import Enrollment
from finance.models import TuitionFee

from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds the database with fake data for testing.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        # Order of deletion is important due to dependencies
        TuitionFee.objects.all().delete()
        Enrollment.objects.all().delete()
        Class.objects.all().delete()
        Course.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write("Creating new data...")
        fake = Faker('fa_IR') # Use Persian Faker for more realistic names

        # --- Create Users and Profiles ---
        self.stdout.write("Creating users and profiles...")

        # Create an admin user
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        admin_user.first_name = 'مدیر'
        admin_user.last_name = 'سیستم'
        admin_user.save()
        admin_user.profile.role = Profile.Role.ADMIN
        admin_user.profile.phone_number = fake.phone_number()
        admin_user.profile.save()

        # Create teachers
        teachers = []
        for i in range(5):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"teacher_{first_name.lower()}_{i}"
            user = User.objects.create_user(username, f'{username}@example.com', 'password123')
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user.profile.role = Profile.Role.TEACHER
            user.profile.phone_number = fake.phone_number()
            user.profile.save()
            teachers.append(user)

        # Create parents and students
        students = []
        for i in range(20):
            # Create parent
            parent_first_name = fake.first_name()
            parent_last_name = fake.last_name()
            parent_username = f"parent_{parent_first_name.lower()}_{i}"
            parent_user = User.objects.create_user(parent_username, f'{parent_username}@example.com', 'password123')
            parent_user.first_name = parent_first_name
            parent_user.last_name = parent_last_name
            parent_user.save()
            parent_user.profile.role = Profile.Role.PARENT
            parent_user.profile.phone_number = fake.phone_number()
            parent_user.profile.save()

            # Create student linked to parent
            student_first_name = fake.first_name()
            student_last_name = parent_last_name # Same last name
            student_username = f"student_{student_first_name.lower()}_{i}"
            student_user = User.objects.create_user(student_username, f'{student_username}@example.com', 'password123')
            student_user.first_name = student_first_name
            student_user.last_name = student_last_name
            student_user.save()
            student_user.profile.role = Profile.Role.STUDENT
            student_user.profile.phone_number = fake.phone_number()
            student_user.profile.parent = parent_user.profile
            student_user.profile.save()
            students.append(student_user)

        # --- Create Courses and Classes ---
        self.stdout.write("Creating courses and classes...")
        course_titles = ["آموزش پایتون مقدماتی", "طراحی وب با Django", "مبانی داده‌کاوی", "یادگیری ماشین پیشرفته", "شبکه‌های کامپیوتری"]
        classes = []
        for title in course_titles:
            course = Course.objects.create(
                title=title,
                description=fake.paragraph(nb_sentences=5),
                base_tuition_fee=random.choice([2000000, 3000000, 5000000])
            )

            start_date = fake.date_object()
            new_class = Class.objects.create(
                course=course,
                instructor=random.choice(teachers),
                title=f"گروه {random.choice(['A', 'B'])} - {random.choice(['صبح', 'عصر'])}",
                capacity=random.randint(10, 20),
                start_date=start_date,
                end_date=start_date + timedelta(days=90),
                start_time=random.choice(['09:00', '14:00']),
                end_time=random.choice(['12:00', '17:00']),
                days_of_week=random.choice(["شنبه, دوشنبه", "یکشنبه, سه‌شنبه"])
            )
            classes.append(new_class)

        # --- Enroll Students in Classes ---
        self.stdout.write("Enrolling students...")
        for student in students:
            # Enroll each student in 1 or 2 classes
            classes_to_enroll = random.sample(classes, k=random.randint(1, 2))
            for klass in classes_to_enroll:
                # Avoid enrolling if class is full
                if klass.enrollments.count() < klass.capacity:
                    enrollment = Enrollment.objects.create(student=student, enrolled_class=klass)

                    # Create tuition fee for the enrollment
                    TuitionFee.objects.create(
                        enrollment=enrollment,
                        total_amount=klass.get_tuition_fee(),
                        due_date=klass.start_date + timedelta(days=7)
                    )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))
