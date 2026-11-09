from django.urls import path

from . import views

app_name = 'messaging'
urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('new/<int:item_pk>/', views.start_conversation, name='start_conversation'),
]
