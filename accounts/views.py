from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegistrationForm


def register(request):
	if request.user.is_authenticated:
		return redirect('chat:inbox')
	form = RegistrationForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		user = form.save()
		login(request, user)
		messages.success(request, 'Your account is ready.')
		return redirect('chat:inbox')
	return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
	if request.method == 'POST':
		request.user.email = request.POST.get('email', '').strip()
		request.user.phone_number = request.POST.get('phone_number', '').strip()
		request.user.save(update_fields=['email', 'phone_number'])
		messages.success(request, 'Profile updated.')
	return render(request, 'accounts/profile.html')
