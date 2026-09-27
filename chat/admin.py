from django.contrib import admin

from .models import Chat, ChatParticipant, Message

admin.site.register(Chat)
admin.site.register(ChatParticipant)
admin.site.register(Message)
