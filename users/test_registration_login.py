from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class RegistrationLoginTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_new_user_registration_logs_in_automatically(self):
        """
        Test that a newly registered user is automatically logged in.
        """
        response = self.client.post(reverse('register'), {
            'username': 'new_user',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': 'reader'
        }, follow=True)
        
        # Should redirect to article-list
        self.assertRedirects(response, reverse('article-list'))
        
        # User should be authenticated in session
        self.assertIn('_auth_user_id', self.client.session)
        
        # Verify the user exists and has the correct role
        user = User.objects.get(username='new_user')
        self.assertTrue(user.is_reader)
        self.assertEqual(user.role, 'reader')
        
        print("[PASS] New user registration automatically logs in the user.")

    def test_existing_user_new_role_registration_logs_in_automatically(self):
        """
        Test that an existing user registering for a new role is automatically logged in with that role.
        """
        # Create a user first
        user = User.objects.create_user(username='existing_user', password='testpass123', is_reader=True, role='reader')
        
        # Register for journalist role
        response = self.client.post(reverse('register'), {
            'username': 'existing_user',
            'password1': 'testpass123',
            'role': 'journalist'
        }, follow=True)
        
        # Should redirect to article-list
        self.assertRedirects(response, reverse('article-list'))
        
        # User should be authenticated
        self.assertIn('_auth_user_id', self.client.session)
        
        # Verify role updated
        user.refresh_from_db()
        self.assertTrue(user.is_journalist)
        self.assertEqual(user.role, 'journalist')
        
        print("[PASS] Existing user registering for new role automatically logs in with the new role.")
