from .models import Message


def unread_messages_count(request):
    """Add unread message count to template context."""
    if request.user.is_authenticated:
        count = Message.objects.filter(
            conversation__in=request.user.buying_conversations.all() | request.user.selling_conversations.all(),
            is_read=False
        ).exclude(sender=request.user).count()
        return {'unread_messages_count': count}
    return {'unread_messages_count': 0}
