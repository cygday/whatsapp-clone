import uuid

from django.conf import settings
from django.db import models


class GroupChat(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	invite_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_groups', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name


class GroupMember(models.Model):
	ROLE_CHOICES = [('member', 'Member'), ('admin', 'Admin'), ('creator', 'Creator')]
	group = models.ForeignKey(GroupChat, related_name='members', on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='group_memberships', on_delete=models.CASCADE)
	role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
	joined_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		constraints = [models.UniqueConstraint(fields=['group', 'user'], name='unique_group_member')]

	def __str__(self):
		return f'{self.user} in {self.group}'


class GroupMessage(models.Model):
	group = models.ForeignKey(GroupChat, related_name='messages', on_delete=models.CASCADE)
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='group_messages', on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created_at']

	def __str__(self):
		return f'Message {self.pk} in {self.group}'
