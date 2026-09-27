from urllib.parse import urlsplit

from django import forms
from django.core.exceptions import ValidationError

from .models import ExternalWhatsAppLink


class ExternalWhatsAppLinkForm(forms.ModelForm):
	class Meta:
		model = ExternalWhatsAppLink
		fields = ['title', 'url']
		widgets = {
			'title': forms.TextInput(attrs={'maxlength': 120, 'placeholder': 'Optional name'}),
			'url': forms.URLInput(attrs={'placeholder': 'https://chat.whatsapp.com/...', 'required': True}),
		}

	def clean_url(self):
		url = self.cleaned_data['url']
		parts = urlsplit(url)
		host = (parts.hostname or '').lower()
		path = parts.path.strip('/')
		is_group_invite = host == 'chat.whatsapp.com' and bool(path)
		is_channel_link = host in {'whatsapp.com', 'www.whatsapp.com'} and path.startswith('channel/') and len(path.split('/')) > 1
		if parts.scheme != 'https' or parts.netloc.lower() != host or not (is_group_invite or is_channel_link):
			raise ValidationError('Enter an HTTPS WhatsApp group invite or channel link.')
		return url