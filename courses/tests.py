from django.test import TestCase
from django.contrib.auth.models import User
from .models import Course, Class
from decimal import Decimal
import jdatetime

class CourseAndClassModelTest(TestCase):
    def setUp(self):
        self.instructor_user = User.objects.create_user(
            username='testinstructor', password='password'
        )
        self.instructor_user.profile.role = 'TEACHER'
        self.instructor_user.profile.save()

        self.course = Course.objects.create(
            title="Test Course",
            description="A course for testing.",
            base_tuition_fee=Decimal('1000000')
        )

    def test_class_creation(self):
        """Test creating a Class instance."""
        klass = Class.objects.create(
            course=self.course,
            instructor=self.instructor_user,
            title="Test Group",
            capacity=15,
            start_date=jdatetime.date(1403, 1, 1),
            end_date=jdatetime.date(1403, 4, 1),
            start_time='09:00',
            end_time='11:00',
            days_of_week="Saturday, Monday"
        )
        self.assertEqual(klass.course.title, "Test Course")
        self.assertEqual(klass.instructor.username, "testinstructor")
        self.assertEqual(str(klass), "Test Course - Test Group")

    def test_get_tuition_fee_method(self):
        """Test the get_tuition_fee method on the Class model."""
        # Case 1: No custom fee, should use course base fee
        klass_no_custom_fee = Class.objects.create(
            course=self.course,
            instructor=self.instructor_user,
            title="Group A",
            capacity=10,
            start_date=jdatetime.date(1403, 1, 1),
            end_date=jdatetime.date(1403, 4, 1),
            start_time='09:00',
            end_time='11:00',
            days_of_week="Saturday, Monday"
        )
        self.assertEqual(klass_no_custom_fee.get_tuition_fee(), self.course.base_tuition_fee)

        # Case 2: Custom fee is set, should override course base fee
        custom_fee = Decimal('1200000')
        klass_with_custom_fee = Class.objects.create(
            course=self.course,
            instructor=self.instructor_user,
            title="Group B",
            capacity=10,
            start_date=jdatetime.date(1403, 1, 1),
            end_date=jdatetime.date(1403, 4, 1),
            start_time='09:00',
            end_time='11:00',
            days_of_week="Sunday, Tuesday",
            custom_tuition_fee=custom_fee
        )
        self.assertEqual(klass_with_custom_fee.get_tuition_fee(), custom_fee)
