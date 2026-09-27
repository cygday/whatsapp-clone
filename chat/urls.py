from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('start/', views.start_chat, name='start'),
    path('links/save/', views.save_external_link, name='save_external_link'),
    path('links/open/', views.open_whatsapp_link, name='open_whatsapp_link'),
    path('links/<int:link_id>/delete/', views.delete_external_link, name='delete_external_link'),
    path('<int:chat_id>/', views.conversation, name='conversation'),
]