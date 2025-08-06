from django.test import TestCase
from django.contrib.auth.models import User
from courses.models import Course, Class
from .models import Enrollment, Attendance
import jdatetime

class EnrollmentAndAttendanceTest(TestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(
            username='teststudent', password='password', first_name='Test', last_name='Student'
        )
        self.student_user.profile.role = 'STUDENT'
        self.student_user.profile.save()

        self.instructor_user = User.objects.create_user(
            username='testinstructor', password='password', first_name='Test', last_name='Instructor'
        )
        self.instructor_user.profile.role = 'TEACHER'
        self.instructor_user.profile.save()

        self.course = Course.objects.create(title="Test Course", base_tuition_fee=1000)
        self.klass = Class.objects.create(
            course=self.course,
            instructor=self.instructor_user,
            title="Test Class",
            capacity=10,
            start_date=jdatetime.date(1403, 1, 1),
            end_date=jdatetime.date(1403, 4, 1),
            start_time='10:00',
            end_time='12:00',
            days_of_week="Mon, Wed"
        )

    def test_student_enrollment(self):
        """Test enrolling a student in a class."""
        enrollment = Enrollment.objects.create(
            student=self.student_user,
            enrolled_class=self.klass
        )
        self.assertEqual(self.klass.enrollments.count(), 1)
        self.assertEqual(enrollment.student, self.student_user)
        self.assertEqual(str(enrollment), "Test Student enrolled in Test Course - Test Class")


    def test_attendance_recording(self):
        """Test recording attendance for an enrollment."""
        enrollment = Enrollment.objects.create(
            student=self.student_user,
            enrolled_class=self.klass
        )
        attendance = Attendance.objects.create(
            enrollment=enrollment,
            session_date=jdatetime.date(1403, 1, 5),
            status=Attendance.Status.PRESENT
        )
        self.assertEqual(enrollment.attendance_records.count(), 1)
        self.assertEqual(attendance.status, Attendance.Status.PRESENT)
        self.assertEqual(str(attendance), f"{enrollment} - 1403-01-05 - Present")
