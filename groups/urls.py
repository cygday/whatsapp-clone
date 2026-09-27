from django.urls import path

from . import views

app_name = 'groups'

urlpatterns = [
    path('create/', views.create_group, name='create'),
    path('invite/<uuid:invite_code>/', views.join_group, name='join'),
    path('<int:group_id>/', views.detail, name='detail'),
    path('<int:group_id>/send/', views.send_message, name='send_message'),
    path('<int:group_id>/members/add/', views.add_member, name='add_member'),
    path('<int:group_id>/leave/', views.leave_group, name='leave'),
]