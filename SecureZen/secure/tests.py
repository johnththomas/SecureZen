from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.test import TestCase, Client

class UserRegistrationFormTestCase(TestCase):
    
    def test_valid_registration_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_invalid_registration_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'invalidemail',
            'password1': 'pass',
            'password2': 'pass'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_duplicate_username_registration_form(self):
        User.objects.create_user('existinguser', 'existing@example.com', 'password123')
        form_data = {
            'username': 'existinguser',
            'email': 'newemail@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

class RegistrationViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('registration')

    def test_registration_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_valid_registration(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302, msg=f"Form errors: {response.context['form'].errors}" if response.status_code != 302 else "")



    def test_invalid_registration(self):
        form_data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password1': 'pass',
            'password2': 'pass'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)  # Stays on the same page due to form errors
        self.assertFalse(User.objects.filter(username='testuser').exists())