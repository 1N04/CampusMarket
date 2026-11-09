from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """A conversation thread between two users about an item."""
    item = models.ForeignKey('listings.Item', on_delete=models.CASCADE, related_name='conversations')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buying_conversations')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='selling_conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        unique_together = ['item', 'buyer']

    def __str__(self):
        return f'{self.buyer} -> {self.seller} about {self.item}'


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    body = models.TextField(verbose_name='Message')
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f'From {self.sender} at {self.sent_at:%Y-%m-%d %H:%M}'
