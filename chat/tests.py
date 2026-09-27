from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from .models import Chat, ChatParticipant, ExternalWhatsAppLink, Message


class ChatTests(TestCase):
	def setUp(self):
		self.alex = CustomUser.objects.create_user(username='alex', password='test-password-42')
		self.blair = CustomUser.objects.create_user(username='blair', password='test-password-42')
		self.chat = Chat.objects.create()
		ChatParticipant.objects.create(chat=self.chat, user=self.alex)
		ChatParticipant.objects.create(chat=self.chat, user=self.blair)

	def test_participant_can_send_message(self):
		self.client.force_login(self.alex)
		response = self.client.post(reverse('chat:conversation', args=[self.chat.pk]), {'content': 'Hello'})
		self.assertRedirects(response, reverse('chat:conversation', args=[self.chat.pk]))
		self.assertEqual(Message.objects.get().content, 'Hello')

	def test_conversation_shows_other_participant(self):
		self.client.force_login(self.alex)
		response = self.client.get(reverse('chat:conversation', args=[self.chat.pk]))
		self.assertContains(response, 'blair')

	def test_nonparticipant_cannot_open_conversation(self):
		stranger = CustomUser.objects.create_user(username='stranger', password='test-password-42')
		self.client.force_login(stranger)
		response = self.client.get(reverse('chat:conversation', args=[self.chat.pk]))
		self.assertEqual(response.status_code, 404)

	def test_user_can_save_whatsapp_group_and_channel_links(self):
		self.client.force_login(self.alex)
		links = [
			('https://chat.whatsapp.com/InviteCode123', 'Study group'),
			('https://whatsapp.com/channel/ChannelCode123?fbclid=example', 'News channel'),
		]
		for url, title in links:
			with self.subTest(url=url):
				response = self.client.post(reverse('chat:save_external_link'), {'url': url, 'title': title})
				self.assertRedirects(response, reverse('chat:inbox'))
		self.assertEqual(ExternalWhatsAppLink.objects.filter(user=self.alex).count(), 2)
		self.assertContains(self.client.get(reverse('chat:inbox')), 'Study group')

	def test_save_rejects_non_whatsapp_and_insecure_links(self):
		self.client.force_login(self.alex)
		for url in ['https://whatsapp.com.attacker.example/channel/abc', 'http://chat.whatsapp.com/InviteCode123']:
			with self.subTest(url=url):
				self.client.post(reverse('chat:save_external_link'), {'url': url})
		self.assertFalse(ExternalWhatsAppLink.objects.exists())

	def test_users_can_only_delete_their_own_saved_links(self):
		link = ExternalWhatsAppLink.objects.create(
			user=self.alex,
			title='Friends',
			url='https://chat.whatsapp.com/InviteCode123',
		)
		self.client.force_login(self.blair)
		response = self.client.post(reverse('chat:delete_external_link', args=[link.pk]))
		self.assertEqual(response.status_code, 404)
		self.assertTrue(ExternalWhatsAppLink.objects.filter(pk=link.pk).exists())

	def test_external_link_landing_accepts_whatsapp_group_invites(self):
		self.client.force_login(self.alex)
		response = self.client.get(reverse('chat:open_whatsapp_link'), {
			'url': 'https://chat.whatsapp.com/InviteCode123',
		})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Open in WhatsApp')
		self.assertContains(response, 'https://chat.whatsapp.com/InviteCode123')

	def test_external_link_landing_rejects_untrusted_urls(self):
		self.client.force_login(self.alex)
		response = self.client.get(reverse('chat:open_whatsapp_link'), {
			'url': 'https://example.com/anything',
		})
		self.assertEqual(response.status_code, 400)
		self.assertNotContains(response, 'Open in WhatsApp', status_code=400)
