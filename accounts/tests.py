from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class AccountTests(TestCase):
	def test_register_creates_user_and_signs_them_in(self):
		response = self.client.post(reverse('register'), {
			'username': 'river',
			'email': 'river@example.com',
			'phone_number': '5550100',
			'password1': 'a-long-test-password-42',
			'password2': 'a-long-test-password-42',
		})
		self.assertRedirects(response, reverse('chat:inbox'))
		self.assertTrue(CustomUser.objects.filter(username='river').exists())
		self.assertEqual(int(self.client.session['_auth_user_id']), CustomUser.objects.get(username='river').id)

	def test_profile_requires_authentication(self):
		response = self.client.get(reverse('profile'))
		self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")
