from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class UserProfileSignalTest(TestCase):
    def test_profile_is_created_for_new_user(self):
        """
        Test that a Profile is automatically created when a new User is created.
        """
        # Create a new user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

        # Check if a profile instance exists for this user
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, Profile)

        # Check the default role
        self.assertEqual(user.profile.role, Profile.Role.STUDENT)

        # Verify it's saved in the database
        profile_from_db = Profile.objects.get(user=user)
        self.assertEqual(profile_from_db, user.profile)
