from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone_number')