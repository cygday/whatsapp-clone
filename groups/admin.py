from django.contrib import admin

from .models import GroupChat, GroupMember, GroupMessage

admin.site.register(GroupChat)
admin.site.register(GroupMember)
admin.site.register(GroupMessage)
