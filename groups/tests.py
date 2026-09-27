from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from .models import GroupChat, GroupMember, GroupMessage


class GroupTests(TestCase):
	def setUp(self):
		self.owner = CustomUser.objects.create_user(username='owner', password='test-password-42')
		self.member = CustomUser.objects.create_user(username='member', password='test-password-42')
		self.group = GroupChat.objects.create(name='Study group', created_by=self.owner)
		GroupMember.objects.create(group=self.group, user=self.owner, role='creator')
		GroupMember.objects.create(group=self.group, user=self.member)

	def test_member_can_send_group_message(self):
		self.client.force_login(self.member)
		response = self.client.post(reverse('groups:send_message', args=[self.group.pk]), {'content': 'Good morning'})
		self.assertRedirects(response, reverse('groups:detail', args=[self.group.pk]))
		self.assertEqual(GroupMessage.objects.get().content, 'Good morning')

	def test_nonmember_cannot_open_group(self):
		outsider = CustomUser.objects.create_user(username='outsider', password='test-password-42')
		self.client.force_login(outsider)
		response = self.client.get(reverse('groups:detail', args=[self.group.pk]))
		self.assertEqual(response.status_code, 404)

	def test_invite_preview_then_join_opens_group(self):
		outsider = CustomUser.objects.create_user(username='outsider', password='test-password-42')
		self.client.force_login(outsider)
		invite_url = reverse('groups:join', args=[self.group.invite_code])
		preview = self.client.get(invite_url)
		self.assertContains(preview, 'Study group')
		response = self.client.post(invite_url)
		self.assertRedirects(response, reverse('groups:detail', args=[self.group.pk]))
		self.assertTrue(GroupMember.objects.get(group=self.group, user=outsider).is_active)

	def test_invite_reactivates_returning_member(self):
		membership = GroupMember.objects.create(group=self.group, user=CustomUser.objects.create_user(username='returning'))
		membership.is_active = False
		membership.save(update_fields=['is_active'])
		self.client.force_login(membership.user)
		response = self.client.post(reverse('groups:join', args=[self.group.invite_code]))
		self.assertRedirects(response, reverse('groups:detail', args=[self.group.pk]))
		membership.refresh_from_db()
		self.assertTrue(membership.is_active)
