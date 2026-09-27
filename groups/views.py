from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import GroupChat, GroupMember, GroupMessage

User = get_user_model()


@login_required
def create_group(request):
	if request.method == 'POST':
		name = request.POST.get('name', '').strip()
		description = request.POST.get('description', '').strip()
		if not name or len(name) > 100:
			messages.error(request, 'Enter a group name of 1 to 100 characters.')
			return redirect('chat:inbox')
		with transaction.atomic():
			group = GroupChat.objects.create(name=name, description=description, created_by=request.user)
			GroupMember.objects.create(group=group, user=request.user, role='creator')
		return redirect('groups:detail', group_id=group.pk)
	return redirect('chat:inbox')


@login_required
def detail(request, group_id):
	group = get_object_or_404(
		GroupChat.objects.prefetch_related('messages__sender', 'members__user'),
		pk=group_id, is_active=True, members__user=request.user, members__is_active=True,
	)
	member = group.members.get(user=request.user, is_active=True)
	return render(request, 'groups/detail.html', {
		'group': group,
		'group_invite_url': request.build_absolute_uri(reverse('groups:join', args=[group.invite_code])),
		'member': member,
		'members': group.members.filter(is_active=True).select_related('user'),
		'group_messages': group.messages.select_related('sender').all(),
		'people': User.objects.filter(is_active=True).exclude(pk__in=group.members.values('user_id')).order_by('username')[:50],
	})


@login_required
def join_group(request, invite_code):
	group = get_object_or_404(GroupChat, invite_code=invite_code, is_active=True)
	membership = GroupMember.objects.filter(group=group, user=request.user).first()
	if request.method == 'POST':
		membership, created = GroupMember.objects.get_or_create(
			group=group,
			user=request.user,
			defaults={'is_active': True},
		)
		if not created and not membership.is_active:
			membership.is_active = True
			membership.save(update_fields=['is_active'])
		return redirect('groups:detail', group_id=group.pk)
	return render(request, 'groups/join.html', {
		'group': group,
		'already_member': membership is not None and membership.is_active,
	})


@login_required
@require_POST
def send_message(request, group_id):
	group = get_object_or_404(GroupChat, pk=group_id, is_active=True)
	if not GroupMember.objects.filter(group=group, user=request.user, is_active=True).exists():
		return redirect('chat:inbox')
	content = request.POST.get('content', '').strip()
	if content:
		GroupMessage.objects.create(group=group, sender=request.user, content=content)
	return redirect('groups:detail', group_id=group.pk)


@login_required
@require_POST
def add_member(request, group_id):
	group = get_object_or_404(GroupChat, pk=group_id, is_active=True)
	if not GroupMember.objects.filter(group=group, user=request.user, is_active=True, role__in=['creator', 'admin']).exists():
		return redirect('groups:detail', group_id=group.pk)
	user = get_object_or_404(User, pk=request.POST.get('user_id'), is_active=True)
	membership, created = GroupMember.objects.get_or_create(group=group, user=user, defaults={'is_active': True})
	if not created and not membership.is_active:
		membership.is_active = True
		membership.save(update_fields=['is_active'])
	return redirect('groups:detail', group_id=group.pk)


@login_required
@require_POST
def leave_group(request, group_id):
	membership = get_object_or_404(GroupMember, group_id=group_id, user=request.user, is_active=True)
	if membership.role == 'creator':
		messages.error(request, 'The group creator cannot leave the group.')
	else:
		membership.is_active = False
		membership.save(update_fields=['is_active'])
		return redirect('chat:inbox')
	return redirect('groups:detail', group_id=group_id)
