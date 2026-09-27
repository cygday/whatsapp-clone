from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
	phone_number = models.CharField(max_length=20, blank=True)
	avatar = models.ImageField(upload_to='avatars/', blank=True)
	is_online = models.BooleanField(default=False)
	last_seen = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.username
