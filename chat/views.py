from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from groups.models import GroupChat, GroupMember
from .forms import ExternalWhatsAppLinkForm
from .models import Chat, ChatParticipant, ExternalWhatsAppLink, Message

User = get_user_model()


@login_required
def inbox(request):
	chats = Chat.objects.filter(participants__user=request.user).prefetch_related(
		'participants__user', 'messages'
	).distinct()
	chat_rows = []
	for chat in chats:
		other = chat.other_participant(request.user)
		if other:
			chat_rows.append((chat, other, chat.messages.last()))
	user_groups = GroupChat.objects.filter(
		members__user=request.user, members__is_active=True, is_active=True
	).distinct()
	people = User.objects.filter(is_active=True).exclude(pk=request.user.pk).order_by('username')[:50]
	return render(request, 'chat/inbox.html', {
		'chat_rows': chat_rows,
		'groups': user_groups,
		'people': people,
		'saved_whatsapp_links': request.user.saved_whatsapp_links.all(),
		'external_link_form': ExternalWhatsAppLinkForm(),
	})


@login_required
@require_POST
def save_external_link(request):
	form = ExternalWhatsAppLinkForm(request.POST)
	if form.is_valid():
		url = form.cleaned_data['url']
		if request.user.saved_whatsapp_links.filter(url=url).exists():
			messages.info(request, 'You have already saved this WhatsApp link.')
		else:
			link = form.save(commit=False)
			link.user = request.user
			link.save()
			messages.success(request, 'WhatsApp link saved.')
	else:
		for error in form.errors.values():
			messages.error(request, error[0])
	return redirect('chat:inbox')


@login_required
@require_POST
def delete_external_link(request, link_id):
	link = get_object_or_404(ExternalWhatsAppLink, pk=link_id, user=request.user)
	link.delete()
	messages.success(request, 'Saved WhatsApp link removed.')
	return redirect('chat:inbox')


@login_required
def open_whatsapp_link(request):
	form = ExternalWhatsAppLinkForm(data={'url': request.GET.get('url', '')})
	if not form.is_valid():
		return render(request, 'chat/open_whatsapp_link.html', {'form': form}, status=400)
	return render(request, 'chat/open_whatsapp_link.html', {
		'whatsapp_url': form.cleaned_data['url'],
		'link_form': ExternalWhatsAppLinkForm(initial={'url': form.cleaned_data['url']}),
	})


@login_required
@require_POST
def start_chat(request):
	recipient = get_object_or_404(User, pk=request.POST.get('recipient_id'), is_active=True)
	if recipient == request.user:
		messages.error(request, 'You cannot start a chat with yourself.')
		return redirect('chat:inbox')
	chat = Chat.objects.filter(participants__user=request.user).filter(
		participants__user=recipient
	).distinct().first()
	if chat is None:
		with transaction.atomic():
			chat = Chat.objects.create()
			ChatParticipant.objects.bulk_create([
				ChatParticipant(chat=chat, user=request.user),
				ChatParticipant(chat=chat, user=recipient),
			])
	return redirect('chat:conversation', chat_id=chat.pk)


@login_required
def conversation(request, chat_id):
	chat = get_object_or_404(Chat, pk=chat_id, participants__user=request.user)
	other = chat.other_participant(request.user)
	if other is None:
		messages.error(request, 'This conversation has no other participant.')
		return redirect('chat:inbox')
	chat_messages = chat.messages.select_related('sender').all()
	if request.method == 'POST':
		content = request.POST.get('content', '').strip()
		if content:
			Message.objects.create(chat=chat, sender=request.user, content=content)
			Chat.objects.filter(pk=chat.pk).update(updated_at=Message.objects.filter(chat=chat).latest('created_at').created_at)
		return redirect('chat:conversation', chat_id=chat.pk)
	return render(request, 'chat/conversation.html', {
		'chat': chat,
		'other': other,
		'chat_messages': chat_messages,
	})
