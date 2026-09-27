from django.conf import settings
from django.db import models


class Chat(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-updated_at']

	def __str__(self):
		return f'Chat {self.pk}'

	def other_participant(self, user):
		membership = self.participants.exclude(user=user).select_related('user').first()
		return membership.user if membership else None


class ChatParticipant(models.Model):
	chat = models.ForeignKey(Chat, related_name='participants', on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chat_memberships', on_delete=models.CASCADE)
	joined_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		constraints = [models.UniqueConstraint(fields=['chat', 'user'], name='unique_chat_participant')]

	def __str__(self):
		return f'{self.user} in {self.chat}'


class Message(models.Model):
	chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	is_read = models.BooleanField(default=False)

	class Meta:
		ordering = ['created_at']

	def __str__(self):
		return f'Message {self.pk} from {self.sender}'


class ExternalWhatsAppLink(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='saved_whatsapp_links', on_delete=models.CASCADE)
	title = models.CharField(max_length=120, blank=True)
	url = models.URLField(max_length=500)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return self.title or self.url
