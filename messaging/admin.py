from django.contrib import admin

from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'seller', 'item', 'created_at', 'updated_at')
    list_select_related = ('buyer', 'seller', 'item')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'sent_at', 'is_read')
    list_filter = ('is_read',)
    list_select_related = ('conversation', 'sender')
